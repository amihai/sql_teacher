import streamlit as st
from frontend.ui.components.layout import Layout
from frontend.ui.components.components import (
    SidebarComponent,
    ChatComponent,
    SessionManagerComponent,
)

st.set_page_config(
    page_title="SQL Teacher",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main app function"""

    layout = Layout()

    sidebar = SidebarComponent()
    session_manager = SessionManagerComponent()
    chat = ChatComponent()

    layout.render([sidebar, session_manager, chat])

if __name__ == "__main__":
    main()