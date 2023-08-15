import os, psycopg2
from iagenda import IAgenda
from contato import Contato
import pandas

class Agenda(IAgenda):
    def __init__(self):
        self.connection = psycopg2.connect(
            host=os.environ['postgres$server'],
            user=os.environ['postgres$user'],
            password=os.environ['postgres$password']
        )

        self.__criar_agenda()

    def digitarContato(self) -> None:
        contato = Contato()
        contato.nome = input("Nome: ")
        contato.telefone = input("Telefone: ")
        print("Email: ", end="")
        contato.email = input()

        return contato

    def listar_contatos(self) -> None:
        dataframe = pandas.read_sql_table("Agenda", self.connection)
        print(dataframe)

    def __criar_agenda(self) -> None:
        sql = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_name like 'agenda'
        """
        cursor = self.connection.cursor()
        cursor.execute(sql)
        ok = cursor.rowcount > 0
        cursor.close()

        if ok: return

        sql = """
        CREATE TABLE agenda (
            telefone VARCHAR(20) PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(256) NULL UNIQUE
        );

        ALTER TABLE agenda ADD nascimento DATE check (nascimento IS NULL OR nascimento >= '1960-01-01');
        
        CREATE INDEX nome ON agenda (nome, nascimento DESC);
        """
        cursor = self.connection.cursor()
        cursor.execute(sql)
        cursor.close()

    def apagar_agenda(self) -> None:
        sql = "DROP TABLE agenda;"

        cursor = self.connection.cursor()
        cursor.execute(sql)
        cursor.close()

        self.__criar_agenda()

    def contatos(self) -> list[Contato]:
        sql = """
        SELECT
        nome,
        telefone,
        email,
        nascimento
        FROM agenda
        ORDER BY
        nome,
        nascimento DESC
        """

        cursor = self.connection.cursor()
        cursor.execute(sql)
        contatos: list[Contato] = []
        for registro in cursor.fetchall():
            contato: Contato = Contato(contato = registro)
            contatos.append(contato)

        cursor.close()

        return contatos


    # @classmethod
    def gravar_contato(self, contato: Contato) -> bool:
        sql = """
        SELECT nome, telefone, email
        FROM agenda
        WHERE
        telefone <> %s AND email = %s
        """
        cursor = self.connection.cursor()
        argumentos = (contato.telefone, contato.email)
        cursor.execute(sql, argumentos)
        novo_contato = cursor.rowcount == 0
        cursor.close()

        if not novo_contato:
            mensagem = "Email %s já cadastrado para o Contato %s, telefone %s"
            mensagem = mensagem % (contato.email, contato.nome, contato.telefone)
            raise Exception(mensagem)

        sql = "SELECT telefone FROM agenda WHERE telefone = %s"
        cursor = self.connection.cursor()
        cursor.execute(sql, (contato.telefone,))
        novo_contato = cursor.rowcount == 0
        cursor.close()

        sql = "UPDATE agenda SET nome = %s, email = %s, nascimento = %s WHERE telefone = %s"
        if novo_contato:
            sql = "INSERT INTO agenda (nome, email, nascimento, telefone) VALUES (%s, %s, %s, %s)"

        argumentos = (contato.nome, contato.email, contato.nascimento, contato.telefone)
        cursor = self.connection.cursor()
        cursor.execute(sql, argumentos)
        self.connection.commit()
        cursor.close()

        return novo_contato

    def carregar_contatos(self, path, ignorar_erros: bool = False) -> None:
        with open(file = path, mode = 'r', encoding = "UTF-8") as file:
            lines = file.readlines()
            lines = ((i, line) for i, line in enumerate(lines) if i > 0)
            file.close()

        if not ignorar_erros:
            for i, line in lines:
                Contato(contato = line.split(";"))
        
        for i, line in lines:
            try:
                contato = Contato(contato = line.split(";"))
                self.gravar_contato(contato)
            except Exception as error:
                message = f"{error} Linha {i}"
                print(error)


    def exportar_contatos(self, path: str, contatos: list[Contato]) -> None:
        with open(file = path, mode = "w") as file:
            for contato in contatos:
                file.write(str(contato) + '\n')

            file.close()

    def apagar_contato(self, contato: Contato) -> bool:
        cursor = self.connection.cursor()
        sql = "DELETE FROM agenda WHERE telefone = %s OR email = %s"
        argumentos = (contato.telefone, contato.email)
        cursor.execute(sql, argumentos)
        result = cursor.rowcount > 0
        cursor.close()
        self.connection.commit()
        return result

    def count(self) -> int:
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) AS counter FROM agenda")
        registro = cursor.fetchone()
        cursor.close()
        return registro[0]


    @staticmethod
    def executar() -> None:
        agenda = Agenda()
        agenda.__criar_agenda()
        agenda.carregar_contatos("contatos.txt")
