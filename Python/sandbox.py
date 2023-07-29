def vogais(palavra):
    contador = 0
    palavra = palavra.lower()
    vogais = "aeiouáàãâäéèêëíìîïóòôõöúùûü"
    for letra in palavra:
        contador = contador + (1 if letra in vogais else 0)

    return contador

def palindroma(palavra):
    palavra = palavra.lower()
    pivot = len(palavra)
    
    if pivot <= 2: return False
    
    pivot = pivot // 2 + 1
    meia_palavra = palavra[0:pivot]
    for i, letra in enumerate(meia_palavra):
        if letra != palavra[-(i + 1)]: return False
        # print(f'{i} {letra} {palavra[-(i + 1)]}')

    return True
