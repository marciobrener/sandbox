from abc import ABC, ABCMeta, abstractmethod

from contato import Contato
    
class IAgenda(ABC):
    @abstractmethod
    def apagar_agenda(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def digitarContato(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def listar_contatos(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def gravar_contato(self, contato: Contato) -> bool:
        raise NotImplementedError

    @abstractmethod
    def carregar_contatos(self, path, ignorar_erros: bool = False) -> None:
        raise NotImplementedError

    @abstractmethod
    def exportar_contatos(self, path: str, contatos: list[Contato]) -> None:
        raise NotImplementedError

    @abstractmethod
    def apagar_contato(self, contato: Contato) -> bool:
        raise NotImplementedError

    @abstractmethod
    def contatos(self) -> list[Contato]:
        raise NotImplementedError

    @abstractmethod
    def count(self) -> int:
        raise NotImplementedError

    def executar() -> None:
        pass

