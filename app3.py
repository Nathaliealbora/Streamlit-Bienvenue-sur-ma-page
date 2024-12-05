import streamlit as st
import pandas as pd
from streamlit_authenticator import Authenticate
from streamlit_option_menu import option_menu 

df = pd.read_csv("users.csv")

users_data = {
    'usernames': {row['name']: {
        'name': row['name'],
        'password': row['password'],
        'email': row['email'],
        'failed_login_attempts': row['failed_login_attempts'],
        'logged_in': row['logged_in'],
        'role': row['role']} for _, row in df.iterrows()}
}

authenticator = Authenticate(
    users_data, 
    "cookie_name",  
    "cookie_key",  
    30  
)

def login():
    authenticator.login()

    if st.session_state["authentication_status"]:
        st.sidebar.write(f"Bienvenue {st.session_state['username']}!")
        authenticator.logout("Déconnexion")
        show_dashboard()
    elif st.session_state["authentication_status"] is False:
        st.error("Identifiants incorrects.")
    elif st.session_state["authentication_status"] is None:
        st.warning("Veuillez vous connecter.")

def show_dashboard():
    selection = sidebar_menu()
    
    if selection == "Accueil":
        st.title("Page d'accueil")
        st.write("Bienvenue sur la page d'accueil de l'application.")
    elif selection == "Photos":
        st.title("Album photo")
        show_cat_images() 
    elif selection == "Profil":
        st.title("Mon Profil")
        st.write(f"Nom: {st.session_state['username']}")
        st.write(f"Email: {df[df['name'] == st.session_state['username']]['email'].values[0]}")

def show_cat_images():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image("images/chat1.jpg", caption="Chat 1")
    
    with col2:
        st.image("images/chat2.jpg", caption="Chat 2")
    
    with col3:
        st.image("images/chat3.jpg", caption="Chat 3")

def sidebar_menu():
    with st.sidebar:
        selection = option_menu(
            menu_title="Menu", 
            options=["Accueil", "Photos", "Profil"], 
            icons=["house", "image", "person"],  
            menu_icon="cast",  
            default_index=0  
        )
    return selection

if __name__ == "__main__":
    login()
