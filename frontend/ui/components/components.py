import streamlit as st
from frontend.ui.components.base import BaseComponent
from frontend.services.adk_service import ADKService
from frontend.helpers.get_conversation import get_conversations, get_first_user_question
from frontend.helpers.terms import terms_and_conditions

print("running...")
print(st.session_state)


class SidebarComponent(BaseComponent):
    """Sidebar component for server configuration"""

    def __init__(self):
        super().__init__("sidebar")
        self.is_sidebar = True

    def initialize_state(self):
        if 'adk_client' not in st.session_state:
            st.session_state.adk_client = None

    def render(self):
        st.title("SQL Teacher")

        try:
            # Only initialize if not already done
            if st.session_state.adk_client is None:
                st.session_state.adk_client = ADKService()
                self.set_state("client_initialized", True)
        except Exception as e:
            self.set_state("client_initialized", False)


class SessionManagerComponent(BaseComponent):
    """Component for managing conversation sessions"""

    def __init__(self):
        super().__init__("session_manager")
        self.is_sidebar = True

    def initialize_state(self):
        if 'current_session_id' not in st.session_state:
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
            return

        if not st.session_state.sessions_loaded or st.button("🔄 Refresh Sessions", key="refresh_sessions"):
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

        # update on changes
        index_of_session_conversation = st.session_state.all_session_conversations.index(selected_session)
        new_session_id = st.session_state.all_session_ids[index_of_session_conversation]

        if new_session_id != st.session_state.current_session_id:
            st.session_state.current_session_id = new_session_id

        col1, col2 = st.columns(2)
        with col1:
            if st.button("New Session", key="new_session_btn"):
                self._create_new_session()

        with col2:
            if st.button("Delete Session", key="delete_session_btn",
                         disabled=not st.session_state.current_session_id):
                self._delete_session()

    @staticmethod
    def _load_sessions():
        """Load all sessions from the service"""
        try:
            sessions = st.session_state.adk_client.get_sessions()
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
        except Exception as e:
            st.error(f"Error loading sessions: {e}")

    @staticmethod
    def _create_new_session():
        """Create a new conversation session"""
        try:
            session = st.session_state.adk_client.create_session()
            st.session_state.current_session_id = session["id"]
            st.session_state.sessions_loaded = False
            st.success(f"Created new session: {session['id'][:8]}...")
            st.rerun()
        except Exception as e:
            st.error(f"Error creating session: {e}")

    @staticmethod
    def _delete_session():
        """Delete the current session"""
        try:
            if st.session_state.current_session_id:
                st.session_state.adk_client.delete_session(session_id=st.session_state.current_session_id)
                st.session_state.current_session_id = None
                st.session_state.sessions_loaded = False  # Mark for reload
                st.rerun()
        except Exception as e:
            st.error(f"Error deleting session: {e}")


class ChatComponent(BaseComponent):
    """Main chat interface component"""

    def __init__(self):
        super().__init__("chat")
        self.is_sidebar = False

    def initialize_state(self):
        if 'cached_conversation' not in st.session_state:
            st.session_state.cached_conversation = None
        if 'cached_session_id' not in st.session_state:
            st.session_state.cached_session_id = None

    def render(self):
        if not st.session_state.adk_client:
            st.info("Please configure server connection in the sidebar")
            return

        if st.session_state.current_session_id:
            self._render_conversation()
        else:
            st.info("Please select or create a session to start chatting")

        self._render_chat_input()

    @staticmethod
    def _render_conversation():
        """Render the current conversation with caching"""

        # get conversation if session changed or cache is empty
        if (st.session_state.cached_session_id != st.session_state.current_session_id or
                st.session_state.cached_conversation is None):

            selected_session = st.session_state.adk_client.get_session_by_id(
                st.session_state.current_session_id
            )
            conversations = get_conversations(selected_session)

            st.session_state.cached_conversation = conversations
            st.session_state.cached_session_id = st.session_state.current_session_id
        else:
            conversations = st.session_state.cached_conversation

        if conversations:
            st.subheader("Current Conversation")
            for turn in conversations.values():
                if "user" in turn:
                    with st.chat_message("user"):
                        st.write(turn["user"])

                if "model" in turn:
                    with st.chat_message("assistant"):
                        st.write(turn["model"])
        else:
            st.info("There is no conversation within this session")

    def _render_chat_input(self):
        """Render the chat input field"""

        prompt = st.chat_input("Ask me anything...")
        if prompt:
            self._handle_user_message(prompt)

    @staticmethod
    def _handle_user_message(self, message: str):
        """Handle user message and get response"""
        # Create session if needed
        if not st.session_state.current_session_id:
            try:
                session = st.session_state.adk_client.create_session()
                st.session_state.current_session_id = session["id"]
                st.session_state.sessions_loaded = False  # Mark for reload
            except Exception as e:
                st.error(f"Error creating session: {e}")
                return
        # user message
        with st.chat_message("user"):
            st.write(message)

        # agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.adk_client.send_message(
                        st.session_state.current_session_id,
                        message
                    )

                    st.session_state.cached_conversation = None

                    # show response
                    if response:
                        st.write(response)

                    st.rerun()

                except Exception as e:
                    st.error(f"Error processing query: {e}")


class TermsModal(BaseComponent):
    def __init__(self):
        super().__init__("terms_modal")
        self.is_sidebar = False

    def initialize_state(self):
        if 'accepted_terms' not in st.session_state:
            st.session_state.accepted_terms = None

    @st.dialog("Terms and conditions")
    def _modal(self):
        st.markdown(terms_and_conditions)
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Yes, I accept"):
                st.session_state.accepted_terms = True
                st.rerun()

        with col2:
            if st.button("No, I do not accept"):
                st.session_state.accepted_terms = False
                st.rerun()

    def render(self):
        """If no decision render the modal"""
        if st.session_state.get("accepted_terms") is None:
            self._modal()