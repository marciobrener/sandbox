import sandbox

def test_answer():
    palavra = "Márcio"
    vogais = sandbox.vogais(palavra)
    print(f'A palavra {palavra} tem {vogais} vogais')
    assert vogais == 3

def test_palindroma_nao_ok():
    palavra = "marcio"
    palindroma = sandbox.palindroma(palavra)
    assert not palindroma

def test_palindroma_ok():
    palavra = "Ame a Ema"
    palindroma = sandbox.palindroma(palavra)
    assert palindroma
