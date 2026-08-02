import streamlit as st
import pandas as pd
from pathlib import Path

from pages.utils.cards import mostrar_card
from pages.utils.planificador import generar_recorrido
from pages.utils.recorrido_state import (
    guardar_recorrido,
    obtener_recorrido,
    existe_recorrido,
    iniciar_visitados
)

# --------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------

st.set_page_config(
    page_title="Recorrido",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Generador de Recorridos")

# --------------------------------------------------
# CARGAR EXCEL
# --------------------------------------------------

archivo = Path("pages") / "datos" / "TOTAL MEDICOS OK.xlsx"

if not archivo.exists():
    st.error("No se encontró el archivo Excel.")
    st.stop()

df = pd.read_excel(archivo)

df.columns = df.columns.str.strip()

df = df.fillna("")

# --------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------

st.subheader("Configuración")

col1, col2, col3 = st.columns(3)

with col1:

    dia = st.selectbox(
        "Día",
        [
            "Lunes",
            "Martes",
            "Miércoles",
            "Jueves",
            "Viernes"
        ]
    )

with col2:

    zona = st.selectbox(
        "Zona",
        [
            "Todas",
            "Haedo",
            "Hurlingham",
            "Villa Tesei",
            "Villa Sarmiento",
            "Parque Leloir",
            "Ituzaingó"
        ]
    )

with col3:

    cantidad = st.number_input(
        "Cantidad máxima",
        min_value=0,
        max_value=100,
        value=13
    )

# --------------------------------------------------
# GENERAR RECORRIDO
# --------------------------------------------------

if st.button("🚗 Generar recorrido", use_container_width=True):

    dias = {
        "Lunes": "Lun",
        "Martes": "Mar",
        "Miércoles": "Mier",
        "Jueves": "Juev",
        "Viernes": "Vier"
    }

    texto = dias[dia]

    filtro = pd.Series(False, index=df.index)

    if "DIA 1" in df.columns:
        filtro |= df["DIA 1"].astype(str).str.contains(texto, case=False)

    if "DIA 2" in df.columns:
        filtro |= df["DIA 2"].astype(str).str.contains(texto, case=False)

    recorrido = df[filtro].copy()

    if zona != "Todas":

        recorrido = recorrido[
            recorrido["DOMICILIO"]
            .astype(str)
            .str.contains(zona, case=False)
        ]

    recorrido = generar_recorrido(recorrido)

    if cantidad > 0:
        recorrido = recorrido.head(cantidad)

    guardar_recorrido(recorrido)

# --------------------------------------------------
# MOSTRAR RECORRIDO
# --------------------------------------------------

if existe_recorrido():

    iniciar_visitados()

    recorrido = obtener_recorrido()

    visitados = len(st.session_state["visitados"])

    total = len(recorrido)

    pendientes = max(total - visitados, 0)

    porcentaje = 0

    if total > 0:
        porcentaje = visitados / total

    st.subheader("📊 Resumen del recorrido")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("👨‍⚕️ Total", total)

    with c2:
        st.metric("✅ Visitados", visitados)

    with c3:
        st.metric("⏳ Pendientes", pendientes)

    st.progress(porcentaje)

    st.success(
        f"Se encontraron {total} médicos."
    )

    st.divider()

    grupo_actual = ""

    for _, medico in recorrido.iterrows():

        if medico["GRUPO"] != grupo_actual:

            grupo_actual = medico["GRUPO"]

            st.header("📍 " + grupo_actual)

        mostrar_card(medico)

        st.divider()