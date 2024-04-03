import streamlit as st

def page2():
    st.title("Página de Registro")
    st.write("Contenido de la página de Registro")
    if st.button("Ir a la página principal"):
        st.session_state.page = "main"
        