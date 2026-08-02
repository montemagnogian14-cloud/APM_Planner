import streamlit as st
import urllib.parse

from pages.utils.recorrido_state import (
    marcar_visitado,
    fue_visitado
)

from pages.utils.excel_manager import guardar_visita


def mostrar_card(medico):

    nombre = str(medico["NOMBRE"])
    especialidad = str(medico["ESPECIALIDAD"])
    domicilio = str(medico["DOMICILIO"])
    ultima = str(medico["ULT VISITA"])

    maps = (
        "https://www.google.com/maps/search/?api=1&query="
        + urllib.parse.quote(domicilio)
    )

    waze = (
        "https://waze.com/ul?q="
        + urllib.parse.quote(domicilio)
    )

    with st.container(border=True):

        st.subheader("👨‍⚕️ " + nombre)

        st.write("**🩺 Especialidad:**", especialidad)

        st.write("**📍 Dirección:**")
        st.write(domicilio)

        st.write("**🗓 Última visita:**", ultima)

        col1, col2, col3 = st.columns(3)

        with col1:

            st.link_button(
                "🗺 Google Maps",
                maps,
                use_container_width=True
            )

        with col2:

            st.link_button(
                "🚗 Waze",
                waze,
                use_container_width=True
            )

        with col3:

            if fue_visitado(nombre):

                st.success("✅ VISITADO")

            else:

                if st.button(
                    "✔ Visitado",
                    key=f"visitado_{nombre}"
                ):

                    ok = guardar_visita(nombre)

                    if ok:

                        marcar_visitado(nombre)

                        st.rerun()

                    else:

                        st.error("No se pudo guardar la visita.")