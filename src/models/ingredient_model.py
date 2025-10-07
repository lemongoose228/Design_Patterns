"""
Модель ингредиента рецепта.
"""
from src.core.validator import ArgumentException, Validator
from src.models.nomenclature_model import NomenclatureModel
from src.models.unit_model import UnitModel


class IngredientModel:
    """
    Модель, представляющая ингредиент в рецепте.
    
    Содержит информацию о продукте, его количестве и единице измерения.
    """

    __nomenclature: NomenclatureModel = None  # Номенклатура продукта
    __quantity: float = 0.0  # Количество ингредиента
    __unit: UnitModel = None  # Единица измерения

    def __init__(self, nomenclature: NomenclatureModel, quantity: float, unit: UnitModel):
        """
        Инициализирует модель ингредиента.
        
        Args:
            nomenclature (NomenclatureModel): Номенклатура продукта
            quantity (float): Количество ингредиента
            unit (UnitModel): Единица измерения количества
        """
        self.nomenclature = nomenclature
        self.quantity = quantity
        self.unit = unit

    @property
    def nomenclature(self) -> NomenclatureModel:
        """
        Получает номенклатуру продукта.
        
        Returns:
            NomenclatureModel: Объект номенклатуры продукта
        """
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: NomenclatureModel):
        """
        Устанавливает номенклатуру продукта с валидацией.
        
        Args:
            value (NomenclatureModel): Номенклатура продукта
            
        Raises:
            ArgumentException: Если передан неверный тип объекта
        """
        if not isinstance(value, NomenclatureModel):
            raise ArgumentException("Номенклатура должна быть экземпляром NomenclatureModel")
        self.__nomenclature = value

    @property
    def quantity(self) -> float:
        """
        Получает количество ингредиента.
        
        Returns:
            float: Количество ингредиента в указанных единицах измерения
        """
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        """
        Устанавливает количество ингредиента с валидацией.
        
        Args:
            value (float): Количество ингредиента
            
        Raises:
            ArgumentException: Если количество не является положительным числом
        """
        Validator.validate_argument(value, (int, float), "quantity")
        if value <= 0:
            raise ArgumentException("Количество должно быть положительным числом")
        self.__quantity = float(value)

    @property
    def unit(self) -> UnitModel:
        """
        Получает единицу измерения.
        
        Returns:
            UnitModel: Объект единицы измерения
        """
        return self.__unit

    @unit.setter
    def unit(self, value: UnitModel):
        """
        Устанавливает единицу измерения с валидацией.
        
        Args:
            value (UnitModel): Единица измерения
            
        Raises:
            ArgumentException: Если передан неверный тип объекта
        """
        if not isinstance(value, UnitModel):
            raise ArgumentException("Единица измерения должна быть экземпляром UnitModel")
        self.__unit = value

    def __str__(self) -> str:
        """
        Строковое представление ингредиента.
        
        Returns:
            str: Ингредиент в формате "наименование - количество единица"
        """
        return f"{self.nomenclature.name} - {self.quantity} {self.unit.name}"