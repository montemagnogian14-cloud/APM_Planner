import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="APM Planner",
    page_icon="💊",
    layout="wide"
)

st.title("💊 APM Planner")

st.write("Bienvenido al sistema de organización de visitas médicas.")

# ---------------------------------------
# CARGAR EXCEL
# ---------------------------------------

archivo = Path("pages") / "datos" / "TOTAL MEDICOS OK.xlsx"

if archivo.exists():

    df = pd.read_excel(archivo)

    df.columns = df.columns.str.strip()

    st.success("Base de datos cargada correctamente.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "👨‍⚕️ Médicos",
            len(df)
        )

    with col2:

        if "ESPECIALIDAD" in df.columns:

            st.metric(
                "🩺 Especialidades",
                df["ESPECIALIDAD"].nunique()
            )

    with col3:

        if "ULT VISITA" in df.columns:

            visitas = df["ULT VISITA"].replace("", pd.NA).count()

            st.metric(
                "📅 Médicos con última visita",
                visitas
            )

else:

    st.error("No se encontró la base de datos.")