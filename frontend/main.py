import streamlit as st
from frontend.ui.components.layout import Layout
from frontend.ui.components.components import (
    SidebarComponent,
    ChatComponent,
    SessionManagerComponent,
    TermsModal,
)

if 'logging_initialized' not in st.session_state:
    from logging_data.logging_config import setup_frontend_logging
    
    # Setup frontend logging with date-based files
    setup_frontend_logging()
    
    st.session_state.logging_initialized = True

# Import logger after initialization
from logging_data.logging_config import get_frontend_logger

logger = get_frontend_logger(__name__)


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
        logger.info("User accepted terms and conditions. Rendering main application.")

        sidebar = SidebarComponent()
        session_manager = SessionManagerComponent()
        chat = ChatComponent()

        layout.render([sidebar, session_manager, chat])

    elif st.session_state.accepted_terms is False:
        logger.warning("User has not accepted terms and conditions. Blocking access to main application.")
        st.error("You have not accepted the terms and conditions. "
                 "If you want to run the application please accept the terms and conditions")
        st.stop()


if __name__ == "__main__":
    main()
