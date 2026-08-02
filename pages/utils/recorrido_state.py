import streamlit as st


def guardar_recorrido(recorrido):
    st.session_state["recorrido"] = recorrido


def obtener_recorrido():
    return st.session_state.get("recorrido")


def existe_recorrido():
    return "recorrido" in st.session_state


def borrar_recorrido():
    st.session_state.pop("recorrido", None)


# -----------------------------------
# VISITADOS
# -----------------------------------

def iniciar_visitados():

    if "visitados" not in st.session_state:

        st.session_state["visitados"] = set()


def marcar_visitado(nombre):

    iniciar_visitados()

    st.session_state["visitados"].add(nombre)


def fue_visitado(nombre):

    iniciar_visitados()

    return nombre in st.session_state["visitados"]