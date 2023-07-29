def capitalize(texto: str) -> str:
    if texto is None or len(texto) < 1: return texto

    result = ""
    for i, letra in enumerate(texto):
        result += (letra.upper() if i == 0 or texto[i - 1] == ' ' else letra)

    return result