import os, sys, tempfile
from iagenda import IAgenda
from agenda import Agenda
from contato import Contato
from util import capitalize

def test_instanciar_agenda() -> None:
    Agenda()

def test_criar_contato_agenda() -> None:
    contato = Contato(
        nome = "nome2",
        telefone = "Telefone",
        email = "Email@email.com"
    )
    contato.nome = 'márcio brener'
    Agenda().gravar_contato(contato)
    assert True

def test_carregar_contatos_sem_ignorar_erros() -> None:
    path = "C:/Backup/Meus Documentos/GitHub/sandbox/contatos.txt"
    result = False

    try:
        Agenda().carregar_contatos(path)

    except Exception as exception:
        result = True

    assert result

def test_carregar_contatos_ignorando_erros() -> None:
    path = "C:/Backup/Meus Documentos/GitHub/sandbox/contatos.txt"
    Agenda().carregar_contatos(path, ignorar_erros=True)
    assert True


def test_criar_arquivo_contatos() -> None:
    path = tempfile.gettempdir() + os.path.sep + 'contatos.tmp'
    contatos : list[Contato] = [
        Contato('nome 1', 'telefone 1', 'email1@email.com'),
        Contato('nome 2', 'telefone 2', 'email2@email.com')
    ]
    
    ok = False
    try:
        Agenda().exportar_contatos(path, contatos)
        ok = True
    except Exception as exception:
        ok = False

    assert ok

def test_instanciar_contato_ok() -> None:
    contato : Contato = Contato(None, None, None, "01/01/1960")
    contato : Contato = Contato("nome", None, "nome@email.com", "\n")
    contato : Contato = Contato()

def test_contato_to_string_ok() -> None:
    contato: Contato = Contato(
        nome=None,
        telefone=None,
        email=None,
        nascimento="01/01/1960"
    )
    line = str(contato)
    ok = line == ";;;01/01/1960"

    contato = Contato("nome", None, "Nome@email.com", "\n")
    line = str(contato)
    ok = ok and line == "Nome;;nome@email.com;"

    contato = Contato()
    line = str(contato)
    ok = ok and line == ";;;"

    assert ok

def test_instanciar_contato_nao_ok() -> None:
    result = False

    try:
        Contato(None, None, "EMAIL")

    except ValueError:
        result = True
    
    assert result

def test_capitalize() -> None:
    print(capitalize('márcio brener costa'))
    assert True

def test_apagar_contato() -> None:
    contato = Contato(
        nome="nome",
        telefone="telefone",
        email="email@dominio.com"
    )

    agenda = Agenda()
    agenda.gravar_contato(contato)
    ok = agenda.apagar_contato(contato)

    assert ok

def test_apagar_agenda() -> None:
    agenda: IAgenda = Agenda()
    agenda.apagar_agenda()
    assert len(agenda.contatos()) == 0

def test_contatos() -> None:
    contatos : list[Contato] = Agenda().contatos()
    assert len(contatos) >= 0

def test_count() -> None:
    ok = Agenda().count() >= 0
    assert ok

def test_main():
    args = sys.argv[1::]
    if len(args) == 0: return

    contato = Contato(contato = args)
    Agenda().gravar_contato(contato)

# if __name__ == '__main__':
#     test_main()