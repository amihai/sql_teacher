import streamlit as st
from frontend.ui.components.layout import Layout
from frontend.ui.components.components import (
    SidebarComponent,
    ChatComponent,
    SessionManagerComponent,
    TermsModal,
)

st.set_page_config(
    page_title="SQL Teacher v1.1",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main app function"""

    layout = Layout()

    terms = TermsModal()
    terms.render()

    if st.session_state.accepted_terms is True:

        sidebar = SidebarComponent()
        session_manager = SessionManagerComponent()
        chat = ChatComponent()

        layout.render([sidebar, session_manager, chat])

    elif st.session_state.accepted_terms is False:
        st.error("You have not accepted the terms and conditions. "
                 "If you want to run the application please accept the terms and conditions")
        st.stop()


if __name__ == "__main__":
    main()
