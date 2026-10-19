def es_bisiesto(anio: int) -> bool:
    return anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0)

def es_fecha_valida(fecha: str) -> bool:
    partes = fecha.split("-")
    if len(partes) != 3:
        return False