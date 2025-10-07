"""
Модель рецепта приготовления блюда.
"""
from src.core.abstract_model import AbstractModel
from src.core.validator import ArgumentException, Validator


class ReceiptModel(AbstractModel):
    """
    Модель, представляющая кулинарный рецепт.
    
    Содержит информацию о рецепте, включая ингредиенты и шаги приготовления.
    Наследует базовую функциональность от AbstractModel.
    """

    __portions: int = 1  # Количество порций
    __cooking_time: str = ""  # Время приготовления
    __ingredients: list = None  # Список ингредиентов
    __cooking_steps: list = None  # Список шагов приготовления

    def __init__(self, name: str = "", portions: int = 1, cooking_time: str = ""):
        """
        Инициализирует модель рецепта.
        
        Args:
            name (str): Название рецепта
            portions (int): Количество порций
            cooking_time (str): Ориентировочное время приготовления
        """
        super().__init__(name)
        self.portions = portions
        self.cooking_time = cooking_time
        self.__ingredients = []
        self.__cooking_steps = []

    @property
    def portions(self) -> int:
        """
        Получает количество порций.
        
        Returns:
            int: Количество порций, на которое рассчитан рецепт
        """
        return self.__portions

    @portions.setter
    def portions(self, value: int):
        """
        Устанавливает количество порций с валидацией.
        
        Args:
            value (int): Количество порций
            
        Raises:
            ArgumentException: Если количество порций не является положительным числом
        """
        Validator.validate_argument(value, int, "portions")
        if value <= 0:
            raise ArgumentException("Количество порций должно быть положительным числом")
        self.__portions = value

    @property
    def cooking_time(self) -> str:
        """
        Получает время приготовления.
        
        Returns:
            str: Описание времени приготовления
        """
        return self.__cooking_time

    @cooking_time.setter
    def cooking_time(self, value: str):
        """
        Устанавливает время приготовления с валидацией.
        
        Args:
            value (str): Время приготовления
            
        Raises:
            ArgumentException: Если описание времени превышает максимальную длину
        """
        Validator.validate_argument(value, str, "cooking_time", max_length=50)
        self.__cooking_time = value.strip()

    @property
    def ingredients(self):
        """
        Получает список ингредиентов.
        
        Returns:
            list: Копия списка ингредиентов рецепта
        """
        return self.__ingredients.copy()

    @property
    def cooking_steps(self):
        """
        Получает список шагов приготовления.
        
        Returns:
            list: Копия списка шагов приготовления рецепта
        """
        return self.__cooking_steps.copy()

    def __str__(self) -> str:
        """
        Строковое представление рецепта.
        
        Returns:
            str: Рецепт в формате "название (порции, время приготовления)"
        """
        return f"{self.name} ({self.portions} порций, {self.cooking_time})"