import streamlit as st
from frontend.ui.components.base import BaseComponent
from frontend.services.adk_service import ADKService
from frontend.helpers.get_conversation import get_conversations, get_first_user_question


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

    def render(self):
        if not st.session_state.adk_client:
            st.warning("Please configure server connection first")
            return

        sessions = st.session_state.adk_client.get_sessions()
        session_ids = [session["id"] for session in sessions]

        all_sessions = [st.session_state.adk_client.get_session_by_id(session["id"]) for session in sessions]
        session_conversations = [get_first_user_question(session) for session in all_sessions]
        print(session_conversations)
        session_ids.insert(0, None)
        session_conversations.insert(0, None)

        st.session_state.all_session_ids = session_ids
        st.session_state.all_session_conversations = session_conversations

        selected_session = st.selectbox(
            "Please select the session",
            options=st.session_state.all_session_conversations,
            key="session_selector",
            index=st.session_state.all_session_ids.index(st.session_state.current_session_id)
        )
        index_of_session_conversation = st.session_state.all_session_conversations.index(selected_session)
        st.session_state.current_session_id = st.session_state.all_session_ids[index_of_session_conversation]
        # print(st.session_state.current_session_id)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("New Session", key="new_session_btn"):
                self._create_new_session()

        with col2:
            if st.button("Delete Session", key="delete_session_btn",
                         disabled=not st.session_state.current_session_id):
                self._delete_session()

    @staticmethod
    def _create_new_session():
        """Create a new conversation session"""
        try:
            session = st.session_state.adk_client.create_session()
            st.session_state.current_session_id = session["id"]
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
                st.session_state.all_session_ids.remove(st.session_state.current_session_id)
                st.session_state.current_session_id = None
                st.rerun()
        except Exception as e:
            st.error(f"Error deleting session: {e}")


class ChatComponent(BaseComponent):
    """Main chat interface component"""

    def __init__(self):
        super().__init__("chat")
        self.is_sidebar = False

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
        """Render the current conversation"""

        selected_session = st.session_state.adk_client.get_session_by_id(
            st.session_state.current_session_id
        )
        conversations = get_conversations(selected_session)

        if conversations:
            st.subheader("Current Conversation")
            for turn in conversations.values():
                for user, message in turn.items():
                    if user == "user":
                        with st.chat_message("user"):
                            st.write(turn["user"])

                    if user == "model":
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
    def _handle_user_message(message: str):
        """Handle user message and get response"""

        if not st.session_state.current_session_id:
            try:
                session = st.session_state.adk_client.create_session()
                st.session_state.current_session_id = session["id"]
                st.success(f"Created new session: {session['id'][:8]}...")
            except Exception as e:
                st.error(f"Error creating session: {e}")
                return

        # Send message
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.adk_client.send_message(
                    st.session_state.current_session_id,
                    message
                )
                st.rerun()
            except Exception as e:
                st.error(f"Error processing query: {e}")
