import datetime
import util

#
class Contato:
    def __init__(self,
                 nome: str = None,
                 telefone: str = None,
                 email: str = None,
                 nascimento: datetime.date = None,
                 contato: list[str] = None):

        if not contato is None:
            nome, telefone, email, nascimento = contato

        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.nascimento = nascimento

    def __str__(self):
        text = '' if self.nascimento is None else "{:02}/{:02}/{:04}".format(
            self.nascimento.day,
            self.nascimento.month,
            self.nascimento.year
        )
             
        contato = [
            '' if self.nome is None else self.nome,
            '' if self.telefone is None else self.telefone,
            '' if self.email is None else self.email,
            text
        ]
        result = ';'.join(contato)
        return result
    
    def get_nome(self):
        return self._nome
    
    def set_nome(self, value):
        self._nome = None if value is None else util.capitalize(value)

    def get_email(self):
        return self._email

    def set_email(self, value) -> None:
        if value is None:
            self._email = value

        elif '@' not in value or ' ' in value:
            raise ValueError(f"Email {value} não contém @ ou contém espaço(s)!")

        else:
            self._email = value.replace('\n', '').lower()

    def get_nascimento(self):
        return self._nascimento

    def set_nascimento(self, value):
        if isinstance(value, datetime.date):
            self._nascimento = value

        elif value is None or value in ['', '\n']:
            self._nascimento = None

        else:
            values = [int(i) for i in value.replace('\n', '').split('/')]
            if (values[0] <= 31):
                values[0], values[1], values[2] = values[2], values[1], values[0]

            year, month, day = values
            self._nascimento = datetime.date(year, month, day)

    nome = property(fget=get_nome, fset=set_nome)
    email = property(fget=get_email, fset=set_email)
    nascimento = property(fget=get_nascimento, fset=set_nascimento)