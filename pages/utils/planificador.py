import pandas as pd

# =====================================================
# INSTITUCIONES
# =====================================================

INSTITUCIONES = {

    "HOSPITAL SAN BERNARDINO": [
        "SAN BERNARDINO"
    ],

    "HOSPITAL GUEMES": [
        "GUEMES",
        "GÜEMES"
    ],

    "RIVADAVIA 1500": [
        "RIVADAVIA 1500"
    ],

    "CIRUGIA": [
        "CIRUGIA",
        "CIRUGÍA"
    ],

    "CLINICA ALCORTA": [
        "ALCORTA"
    ],

    "CLINICA TACHELLA": [
        "TACHELLA"
    ]

}

# =====================================================
# BUSCAR GRUPO
# =====================================================

def obtener_grupo(domicilio):

    texto = str(domicilio).upper()

    for grupo, palabras in INSTITUCIONES.items():

        for palabra in palabras:

            if palabra in texto:

                return grupo

    return "CONSULTORIOS"


# =====================================================
# PRIORIDAD
# =====================================================

def prioridad(grupo):

    if grupo.startswith("HOSPITAL"):
        return 1

    if grupo.startswith("CLINICA"):
        return 2

    if grupo in ["RIVADAVIA 1500", "CIRUGIA"]:
        return 3

    return 4


# =====================================================
# GENERAR RECORRIDO
# =====================================================

def generar_recorrido(df):

    recorrido = df.copy()

    recorrido["GRUPO"] = recorrido["DOMICILIO"].apply(
        obtener_grupo
    )

    recorrido["PRIORIDAD"] = recorrido["GRUPO"].apply(
        prioridad
    )

    recorrido = recorrido.sort_values(
        by=[
            "PRIORIDAD",
            "GRUPO",
            "NOMBRE"
        ]
    )

    return recorrido.drop(
        columns=[
            "PRIORIDAD"
        ]
    )