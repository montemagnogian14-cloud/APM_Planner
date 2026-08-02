from pathlib import Path
from shutil import copy2
from datetime import datetime


def crear_backup():

    origen = Path("pages") / "datos" / "TOTAL MEDICOS OK.xlsx"

    carpeta_backup = Path("pages") / "backup"

    carpeta_backup.mkdir(exist_ok=True)

    fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    destino = carpeta_backup / f"BACKUP_{fecha}.xlsx"

    copy2(origen, destino)

    return destino