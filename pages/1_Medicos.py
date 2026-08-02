import streamlit as st
import pandas as pd
from pathlib import Path

from pages.utils.backup import crear_backup

# --------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------

st.set_page_config(
    page_title="Médicos",
    page_icon="👨‍⚕️",
    layout="wide"
)

st.title("👨‍⚕️ Médicos")

# --------------------------------------------------
# CARGAR EXCEL
# --------------------------------------------------

archivo = Path("pages") / "datos" / "TOTAL MEDICOS OK.xlsx"

if not archivo.exists():
    st.error(f"No se encontró el archivo:\n\n{archivo}")
    st.stop()

df = pd.read_excel(archivo)

df.columns = df.columns.str.strip()

df = df.fillna("")

# --------------------------------------------------
# BUSCADOR
# --------------------------------------------------

buscar = st.text_input("🔍 Buscar médico")

if buscar:

    filtro = (
        df["NOMBRE"].astype(str).str.contains(buscar, case=False)
        |
        df["DOMICILIO"].astype(str).str.contains(buscar, case=False)
        |
        df["ESPECIALIDAD"].astype(str).str.contains(buscar, case=False)
    )

    df = df[filtro]

# --------------------------------------------------
# RESULTADOS
# --------------------------------------------------

st.success(f"Se encontraron {len(df)} médicos.")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# --------------------------------------------------
# BACKUP
# --------------------------------------------------

st.divider()

if st.button("💾 Crear Backup"):

    archivo_backup = crear_backup()

    st.success(
        f"✅ Backup creado correctamente:\n{archivo_backup.name}"
    )