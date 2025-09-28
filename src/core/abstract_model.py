from abc import ABC
import uuid
from src.core.validator import ArgumentException, Validator

class AbstractModel(ABC):
    __id: str = ""
    __name: str = ""

    def __init__(self, name: str = ""):
        super().__init__()
        self.__id = str(uuid.uuid4())
        self.name = name 

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, value: str):
        Validator.validate_argument(value, str, "id", min_length=1)
        self.__id = value.strip()

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        Validator.validate_argument(value, str, "name", max_length=50, min_length=1)
        self.__name = value.strip()

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, AbstractModel):
            return False
        return self.__id == value.id

    def __str__(self) -> str:
        return f"{self.__name} ({self.__id})"