import streamlit as st
import pandas as pd
from pathlib import Path

# ---------------------------------
# CONFIGURACIÓN
# ---------------------------------

st.set_page_config(
    page_title="APM Planner",
    page_icon="🩺",
    layout="wide"
)

# ---------------------------------
# CARGAR EXCEL
# ---------------------------------

archivo = Path("datos") / "TOTAL MEDICOS OK.xlsx"

if not archivo.exists():
    st.error("No encontré el archivo Excel.")
    st.stop()

df = pd.read_excel(archivo)

# ---------------------------------
# TÍTULO
# ---------------------------------

st.title("🩺 Planificador APM")

# ---------------------------------
# BUSCADOR
# ---------------------------------

buscar = st.text_input(
    "🔍 Buscar médico por nombre"
)

# ---------------------------------
# FILTROS
# ---------------------------------

col1, col2 = st.columns(2)

with col1:

    especialidades = ["Todas"] + sorted(
        df["ESPECIALIDAD"]
        .dropna()
        .unique()
        .tolist()
    )

    especialidad = st.selectbox(
        "Especialidad",
        especialidades
    )

with col2:

    dia = st.selectbox(
        "Día",
        [
            "Todos",
            "Lunes",
            "Martes",
            "Miércoles",
            "Jueves",
            "Viernes"
        ]
    )

# ---------------------------------
# FILTRO POR NOMBRE
# ---------------------------------

if buscar != "":

    df = df[
        df["NOMBRE"]
        .fillna("")
        .str.contains(
            buscar,
            case=False
        )
    ]

# ---------------------------------
# FILTRO POR ESPECIALIDAD
# ---------------------------------

if especialidad != "Todas":

    df = df[
        df["ESPECIALIDAD"] == especialidad
    ]

# ---------------------------------
# FILTRO POR DÍA
# ---------------------------------

if dia != "Todos":

    abreviaturas = {
        "Lunes": "Lun",
        "Martes": "Mar",
        "Miércoles": "Mier",
        "Jueves": "Juev",
        "Viernes": "Vier"
    }

    texto = abreviaturas[dia]

    filtro = pd.Series(False, index=df.index)

    if "DIA 1" in df.columns:
        filtro = filtro | df["DIA 1"].fillna("").astype(str).str.contains(texto, case=False)

    if "DIA 2" in df.columns:
        filtro = filtro | df["DIA 2"].fillna("").astype(str).str.contains(texto, case=False)

    df = df[filtro]

# ---------------------------------
# RESULTADOS
# ---------------------------------

st.success(f"Se encontraron {len(df)} médicos.")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)