from pathlib import Path
from datetime import datetime

import pandas as pd

from pages.utils.backup import crear_backup


def guardar_visita(nombre):

    # -------------------------
    # Crear backup
    # -------------------------

    crear_backup()

    # -------------------------
    # Abrir Excel
    # -------------------------

    archivo = Path("pages") / "datos" / "TOTAL MEDICOS OK.xlsx"

    df = pd.read_excel(archivo)

    df.columns = df.columns.str.strip()

    # -------------------------
    # Buscar médico
    # -------------------------

    indice = df[
        df["NOMBRE"].astype(str).str.upper()
        ==
        nombre.upper()
    ].index

    if len(indice) == 0:

        return False

    # -------------------------
    # Escribir fecha
    # -------------------------

    fecha = datetime.now().strftime("%d/%m/%Y")

    df.loc[indice[0], "ULT VISITA"] = fecha

    # -------------------------
    # Guardar Excel
    # -------------------------

    df.to_excel(
        archivo,
        index=False
    )

    return True