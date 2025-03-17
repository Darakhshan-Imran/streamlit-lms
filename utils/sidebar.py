
import streamlit as st
from streamlit_option_menu import option_menu



def sidebar():
    # Sidebar Header
    st.sidebar.image("assets/book_logo.svg", use_container_width=True)

    # Define menu options with icons
    menu_options = [
        ("Home Page", "house"),
        ("Add Book", "book"),
        ("Remove Book", "trash"),
        ("Search a Book", "search"),
        ("Update Book", "pencil"),
        ("My Collection", "folder"),
        ("Reading Stats", "bar-chart"),
    ]

    # Ensure session state is initialized only once
    if "selected_option" not in st.session_state:
        st.session_state.selected_option = "Home Page"

    # Sidebar menu using option_menu
    with st.sidebar:
        selected_option = option_menu(
            menu_title="📚 Library Menu",  # Sidebar title
            options=[item[0] for item in menu_options],  # Extract menu labels
            icons=[item[1] for item in menu_options],  # Extract icons
            menu_icon="list-task",  # Sidebar main icon
            default_index=[item[0] for item in menu_options].index(st.session_state.selected_option),
            orientation="vertical",
            key="menu",  # Assign a unique key to maintain state
            styles={
                "container": {"padding": "5px"},
                "icon": {"color": "#3498db", "font-size": "20px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "5px",
                    "padding": "10px",
                    "border-radius": "8px",
                    "background-color": "#f4f4f4",
                    "color": "#333",
                    "transition": "0.3s",
                },
                "nav-link-selected": {"background-color": "#3498db", "color": "white"},
            }
        )

    # Update session state but REMOVE st.rerun()
    st.session_state.selected_option = selected_option  

    return st.session_state.selected_option  # Return the selected option


