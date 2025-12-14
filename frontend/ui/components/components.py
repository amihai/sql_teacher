import streamlit as st
from typing import Optional
from frontend.ui.components.base import BaseComponent
from frontend.services.adk_service import ADKService
from frontend.helpers.get_conversation import get_conversations, get_first_user_question, extract_model_response_text
from frontend.helpers.terms import terms_and_conditions
from logging_data.logging_config import get_frontend_logger


logger = get_frontend_logger(__name__)

logger.info("Components module loaded")
logger.debug(f"Session state keys: {list(st.session_state.keys())}")

class SidebarComponent(BaseComponent):
    """Sidebar component for server configuration"""

    def __init__(self):
        self.logger = get_frontend_logger(f"{__name__}.{self.__class__.__name__}")
        super().__init__("sidebar")
        self.is_sidebar = True

    def initialize_state(self):
        if 'adk_client' not in st.session_state:
            self.logger.info("Initializing adk_client state")
            st.session_state.adk_client = None

    def render(self):
        st.title("SQL Teacher")

        try:
            if st.session_state.adk_client is None:
                self.logger.info("Creating ADK service instance")
                st.session_state.adk_client = ADKService()
                self.set_state("client_initialized", True)
                self.logger.info("ADK service initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize ADK service: {e}", exc_info=True)
            self.set_state("client_initialized", False)


class SessionManagerComponent(BaseComponent):
    """Component for managing conversation sessions"""

    def __init__(self):
        self.logger = get_frontend_logger(f"{__name__}.{self.__class__.__name__}")
        super().__init__("session_manager")
        self.is_sidebar = True

    def initialize_state(self):
        if 'current_session_id' not in st.session_state:
            self.logger.info("Initializing current_session_id state")
            st.session_state.current_session_id = None

        if 'all_session_ids' not in st.session_state:
            st.session_state.all_session_ids = []

        if 'all_session_conversations' not in st.session_state:
            st.session_state.all_session_conversations = []
        
        if 'sessions_loaded' not in st.session_state:
            st.session_state.sessions_loaded = False

    def render(self):
        if not st.session_state.adk_client:
            st.warning("Please configure server connection first")
            self.logger.warning("Attempted to render sessions without ADK client")
            return

        #  get sessions if needed
        if not st.session_state.sessions_loaded or st.button("🔄 Refresh Sessions", key="refresh_sessions"):
            self.logger.info("Loading sessions...")
            self._load_sessions()
            st.session_state.sessions_loaded = True

        if not st.session_state.all_session_ids:
            st.info("No sessions available")
            if st.button("Create First Session", key="create_first_session"):
                self._create_new_session()
            return

        # default index
        if st.session_state.current_session_id and st.session_state.current_session_id in st.session_state.all_session_ids:
            default_index = st.session_state.all_session_ids.index(st.session_state.current_session_id)
        else:
            default_index = 0

        selected_session = st.selectbox(
            "Please select the session",
            options=st.session_state.all_session_conversations,
            key="session_selector",
            index=default_index,
        )

        # update if selection changed
        index_of_session_conversation = st.session_state.all_session_conversations.index(selected_session)
        new_session_id = st.session_state.all_session_ids[index_of_session_conversation]
        
        if new_session_id != st.session_state.current_session_id:
            self.logger.info(f"Session changed from {st.session_state.current_session_id} to {new_session_id}")
            st.session_state.current_session_id = new_session_id

        col1, col2 = st.columns(2)
        with col1:
            if st.button("New Session", key="new_session_btn"):
                self._create_new_session()

        with col2:
            if st.button("Delete Session", key="delete_session_btn",
                         disabled=not st.session_state.current_session_id):
                self._delete_session()

    def _load_sessions(self):
        """Load all sessions from the service"""
        try:
            self.logger.info("Fetching sessions from ADK service")
            sessions = st.session_state.adk_client.get_sessions()
            self.logger.info(f"Retrieved {len(sessions)} sessions")
            
            session_ids = [session["id"] for session in sessions]

            all_sessions = [st.session_state.adk_client.get_session_by_id(session["id"]) for session in sessions]
            session_conversations = [
                get_first_user_question(session) or f"New session {session['id'][:8]}..." 
                for session in all_sessions
            ]

            session_ids.insert(0, None)
            session_conversations.insert(0, "Choose an option")

            st.session_state.all_session_ids = session_ids
            st.session_state.all_session_conversations = session_conversations
            self.logger.debug(f"Loaded session IDs: {session_ids}")
        except Exception as e:
            self.logger.error(f"Error loading sessions: {e}", exc_info=True)
            st.error(f"Error loading sessions: {e}")

    def _create_new_session(self):
        """Create a new conversation session"""
        try:
            self.logger.info("Creating new session")
            session = st.session_state.adk_client.create_session()
            session_id = session["id"]
            st.session_state.current_session_id = session_id
            st.session_state.sessions_loaded = False  # Mark for reload
            self.logger.info(f"Created new session: {session_id}")
            st.success(f"Created new session: {session_id[:8]}...")
            st.rerun()
        except Exception as e:
            self.logger.error(f"Error creating session: {e}", exc_info=True)
            st.error(f"Error creating session: {e}")

    def _delete_session(self):
        """Delete the current session"""
        try:
            if st.session_state.current_session_id:
                session_id = st.session_state.current_session_id
                self.logger.info(f"Deleting session: {session_id}")
                st.session_state.adk_client.delete_session(session_id=session_id)
                st.session_state.current_session_id = None
                st.session_state.sessions_loaded = False  # Mark for reload
                self.logger.info(f"Successfully deleted session: {session_id}")
                st.rerun()
        except Exception as e:
            self.logger.error(f"Error deleting session: {e}", exc_info=True)
            st.error(f"Error deleting session: {e}")


class ChatComponent(BaseComponent):
    """Main chat interface component"""

    def __init__(self):
        self.logger = get_frontend_logger(f"{__name__}.{self.__class__.__name__}")
        super().__init__("chat")
        self.is_sidebar = False

    def initialize_state(self):
        if 'cached_conversation' not in st.session_state:
            self.logger.info("Initializing cached_conversation state")
            st.session_state.cached_conversation = None
        if 'cached_session_id' not in st.session_state:
            st.session_state.cached_session_id = None

    def render(self):
        if not st.session_state.adk_client:
            st.info("Please configure server connection in the sidebar")
            self.logger.warning("Attempted to render chat without ADK client")
            return

        if st.session_state.current_session_id:
            self._render_conversation()
        else:
            st.info("Please select or create a session to start chatting")
            self.logger.debug("No session selected for chat")

        self._render_chat_input()

    def _render_conversation(self):
        """Render the current conversation with caching"""
        session_id = st.session_state.current_session_id
        
        # get conversation if session changed or cache is empty
        if (st.session_state.cached_session_id != session_id or 
            st.session_state.cached_conversation is None):
            
            self.logger.info(f"Fetching conversation for session: {session_id}")
            selected_session = st.session_state.adk_client.get_session_by_id(session_id)
            conversations = get_conversations(selected_session)
            
            st.session_state.cached_conversation = conversations
            st.session_state.cached_session_id = session_id
            self.logger.debug(f"Cached {len(conversations) if conversations else 0} conversation turns")
        else:
            self.logger.debug(f"Using cached conversation for session: {session_id}")
            conversations = st.session_state.cached_conversation

        if conversations:
            st.subheader("Current Conversation")
            turn_count = 0
            for turn in conversations.values():
                if "user" in turn:
                    with st.chat_message("user"):
                        st.write(turn["user"])
                    turn_count += 1

                if "model" in turn:
                    with st.chat_message("assistant"):
                        st.write(turn["model"])
            
            self.logger.debug(f"Rendered {turn_count} conversation turns")
        else:
            st.info("There is no conversation within this session")
            self.logger.debug("No conversation found in current session")

    def _render_chat_input(self):
        """Render the chat input field"""
        prompt = st.chat_input("Ask me anything...")
        if prompt:
            self.logger.info(f"User submitted message: '{prompt[:50]}...'")
            self._handle_user_message(prompt)

    def _handle_user_message(self, message: str):
        """Handle user message and get response"""
    
        if not st.session_state.current_session_id:
            try:
                self.logger.info("No active session, creating new session for message")
                session = st.session_state.adk_client.create_session()
                st.session_state.current_session_id = session["id"]
                st.session_state.sessions_loaded = False  # Mark for reload
                self.logger.info(f"Created session {session['id']} for incoming message")
            except Exception as e:
                self.logger.error(f"Error creating session for message: {e}", exc_info=True)
                st.error(f"Error creating session: {e}")
                return

        session_id = st.session_state.current_session_id

        # user message
        with st.chat_message("user"):
            st.write(message)

        # agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    self.logger.info(f"Sending message to session {session_id}")
                    
                    response = st.session_state.adk_client.send_message(
                        session_id,
                        message
                    )
                    
                    st.session_state.cached_conversation = None
                    self.logger.debug("Invalidated conversation cache")
                    
                    # Log response for debugging (don't display to avoid JSON flash)
                    if response:
                        response_text = extract_model_response_text(response)
                        self.logger.debug(f"Response text preview: {response_text[:100] if len(response_text) > 100 else response_text}")
                    
                    self.logger.info("Triggering rerun to refresh conversation")
                    st.rerun()
                    
                except Exception as e:
                    self.logger.error(f"Error processing message: {e}", exc_info=True)
                    st.error(f"Error processing query: {e}")


class TermsModal(BaseComponent):
    def __init__(self):
        self.logger = get_frontend_logger(f"{__name__}.{self.__class__.__name__}")
        super().__init__("terms_modal")
        self.is_sidebar = False

    def initialize_state(self):
        if 'accepted_terms' not in st.session_state:
            self.logger.info("Initializing accepted_terms state")
            st.session_state.accepted_terms = None

    @st.dialog("Terms and conditions")
    def _modal(self):
        st.markdown(terms_and_conditions)
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Yes, I accept"):
                self.logger.info("User accepted terms and conditions")
                st.session_state.accepted_terms = True
                st.rerun()

        with col2:
            if st.button("No, I do not accept"):
                self.logger.warning("User declined terms and conditions")
                st.session_state.accepted_terms = False
                st.rerun()

    def render(self):
        """If no decision render the modal"""
        if st.session_state.get("accepted_terms") is None:
            self.logger.debug("Rendering terms and conditions modal")
            self._modal()
        else:
            self.logger.debug(f"Terms already accepted: {st.session_state.accepted_terms}")