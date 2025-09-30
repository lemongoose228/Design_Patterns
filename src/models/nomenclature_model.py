from src.core.abstract_model import AbstractModel
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.models.unit_model import UnitModel
from src.core.validator import ArgumentException, Validator

class NomenclatureModel(AbstractModel):
    __full_name: str = ""
    __group = None
    __unit = None

    def __init__(self, name: str = "", full_name: str = "", group = None, unit = None):
        super().__init__(name)
        self.full_name = full_name
        self.group = group
        self.unit = unit

    @property
    def full_name(self) -> str:
        return self.__full_name

    @full_name.setter
    def full_name(self, value: str):
        Validator.validate_argument(value, str, "full_name", max_length=255)
        self.__full_name = value.strip()

    @property
    def group(self):
        return self.__group

    @group.setter
    def group(self, value):
        if value is not None and not isinstance(value, NomenclatureGroupModel):
            raise ArgumentException("Группа должна быть экземпляром NomenclatureGroupModel")
        self.__group = value

    @property
    def unit(self):
        return self.__unit

    @unit.setter
    def unit(self, value):
        if value is not None and not isinstance(value, UnitModel):
            raise ArgumentException("Единица измерения должна быть экземпляром UnitModel")
        self.__unit = value
