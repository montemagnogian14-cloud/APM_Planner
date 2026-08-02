def prioridad_medico(domicilio):

    texto = str(domicilio).upper()

    if "HOSPITAL" in texto:
        return 1

    if "SANATORIO" in texto:
        return 2

    if "CLINICA" in texto or "CLÍNICA" in texto:
        return 3

    return 4