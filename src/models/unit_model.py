from src.core.abstract_model import AbstractModel
from src.core.validator import ArgumentException, Validator

class UnitModel(AbstractModel):
    __base_unit = None
    __factor: float = 1.0

    def __init__(self, name: str = "", factor: float = 1.0, base_unit = None):
        super().__init__(name)
        self.factor = factor
        self.base_unit = base_unit

    @property
    def base_unit(self):
        return self.__base_unit

    @base_unit.setter
    def base_unit(self, value):
        if value is not None and not isinstance(value, UnitModel):
            raise ArgumentException("Базовая единица измерения должна быть экземпляром UnitModel или None")
        self.__base_unit = value

    @property
    def factor(self) -> float:
        return self.__factor

    @factor.setter
    def factor(self, value: float):
        Validator.validate_argument(value, (int, float), "factor")
        if value <= 0:
            raise ArgumentException("Коэффициент пересчета должен быть положительным числом")
        self.__factor = float(value)