from src.core.abstract_model import AbstractModel
from src.core.validator import ArgumentException, Validator
from src.models.nomenclature_model import NomenclatureModel
from src.models.unit_model import UnitModel

class IngredientModel:
    __nomenclature: NomenclatureModel = None
    __quantity: float = 0.0
    __unit: UnitModel = None

    def __init__(self, nomenclature: NomenclatureModel, quantity: float, unit: UnitModel):
        self.nomenclature = nomenclature
        self.quantity = quantity
        self.unit = unit

    @property
    def nomenclature(self) -> NomenclatureModel:
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: NomenclatureModel):
        if not isinstance(value, NomenclatureModel):
            raise ArgumentException("Номенклатура должна быть экземпляром NomenclatureModel")
        self.__nomenclature = value

    @property
    def quantity(self) -> float:
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        Validator.validate_argument(value, (int, float), "quantity")
        if value <= 0:
            raise ArgumentException("Количество должно быть положительным числом")
        self.__quantity = float(value)

    @property
    def unit(self) -> UnitModel:
        return self.__unit

    @unit.setter
    def unit(self, value: UnitModel):
        if not isinstance(value, UnitModel):
            raise ArgumentException("Единица измерения должна быть экземпляром UnitModel")
        self.__unit = value

    def __str__(self) -> str:
        return f"{self.nomenclature.name} - {self.quantity} {self.unit.name}"

class CookingStepModel:
    __description: str = ""
    __step_number: int = 0

    def __init__(self, step_number: int, description: str):
        self.step_number = step_number
        self.description = description

    @property
    def step_number(self) -> int:
        return self.__step_number

    @step_number.setter
    def step_number(self, value: int):
        Validator.validate_argument(value, int, "step_number")
        if value <= 0:
            raise ArgumentException("Номер шага должен быть положительным числом")
        self.__step_number = value

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, value: str):
        Validator.validate_argument(value, str, "description", max_length=500)
        self.__description = value.strip()

    def __str__(self) -> str:
        return f"{self.step_number}. {self.description}"

class ReceiptModel(AbstractModel):
    __portions: int = 1
    __cooking_time: str = ""
    __ingredients: list[IngredientModel] = None
    __cooking_steps: list[CookingStepModel] = None

    def __init__(self, name: str = "", portions: int = 1, cooking_time: str = ""):
        super().__init__(name)
        self.portions = portions
        self.cooking_time = cooking_time
        self.__ingredients = []
        self.__cooking_steps = []

    @property
    def portions(self) -> int:
        return self.__portions

    @portions.setter
    def portions(self, value: int):
        Validator.validate_argument(value, int, "portions")
        if value <= 0:
            raise ArgumentException("Количество порций должно быть положительным числом")
        self.__portions = value

    @property
    def cooking_time(self) -> str:
        return self.__cooking_time

    @cooking_time.setter
    def cooking_time(self, value: str):
        Validator.validate_argument(value, str, "cooking_time", max_length=50)
        self.__cooking_time = value.strip()

    @property
    def ingredients(self) -> list[IngredientModel]:
        return self.__ingredients.copy()

    def add_ingredient(self, ingredient: IngredientModel):
        if not isinstance(ingredient, IngredientModel):
            raise ArgumentException("Ингредиент должен быть экземпляром IngredientModel")
        self.__ingredients.append(ingredient)

    @property
    def cooking_steps(self) -> list[CookingStepModel]:
        return self.__cooking_steps.copy()

    def add_cooking_step(self, step: CookingStepModel):
        if not isinstance(step, CookingStepModel):
            raise ArgumentException("Шаг приготовления должен быть экземпляром CookingStepModel")
        self.__cooking_steps.append(step)

    def __str__(self) -> str:
        return f"{self.name} ({self.portions} порций, {self.cooking_time})"