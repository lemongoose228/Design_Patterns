from abc import ABC
import uuid
from src.core.validator import ArgumentException, Validator

# Абстрактная базовая модель для всех сущностей
class AbstractModel(ABC):
    __id: str = ""  # Уникальный идентификатор
    __name: str = ""  # Название модели

    def __init__(self, name: str = ""):
        super().__init__()
        self.__id = str(uuid.uuid4())  # Генерация UUID
        self.name = name  # Установка имени через сеттер

    @property
    def id(self) -> str:
        # Геттер для идентификатора
        return self.__id

    @id.setter
    def id(self, value: str):
        # Сеттер для идентификатора с валидацией
        Validator.validate_argument(value, str, "id", min_length=1)
        self.__id = value.strip()

    @property
    def name(self) -> str:
        # Геттер для названия
        return self.__name

    @name.setter
    def name(self, value: str):
        # Сеттер для названия с валидацией
        Validator.validate_argument(value, str, "name", max_length=50, min_length=1)
        self.__name = value.strip()

    def __eq__(self, value: object) -> bool:
        # Сравнение моделей по идентификатору
        if not isinstance(value, AbstractModel):
            return False
        return self.id == value.id

    def __str__(self) -> str:
        # Строковое представление модели
        return f"{self.__name} ({self.__id})"