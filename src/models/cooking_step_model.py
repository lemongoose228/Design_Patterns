"""
Модель шага приготовления рецепта.
"""
from src.core.validator import ArgumentException, Validator


class CookingStepModel:
    """
    Модель, представляющая один шаг в процессе приготовления рецепта.
    
    Содержит информацию о порядке выполнения и описании шага.
    """

    __description: str = ""  # Описание шага приготовления
    __step_number: int = 0  # Порядковый номер шага

    def __init__(self, step_number: int, description: str):
        """
        Инициализирует модель шага приготовления.
        
        Args:
            step_number (int): Порядковый номер шага в рецепте
            description (str): Подробное описание выполнения шага
        """
        self.step_number = step_number
        self.description = description

    @property
    def step_number(self) -> int:
        """
        Получает порядковый номер шага.
        
        Returns:
            int: Порядковый номер шага в последовательности приготовления
        """
        return self.__step_number

    @step_number.setter
    def step_number(self, value: int):
        """
        Устанавливает порядковый номер шага с валидацией.
        
        Args:
            value (int): Порядковый номер шага
            
        Raises:
            ArgumentException: Если номер шага не является положительным числом
        """
        Validator.validate_argument(value, int, "step_number")
        if value <= 0:
            raise ArgumentException("Номер шага должен быть положительным числом")
        self.__step_number = value

    @property
    def description(self) -> str:
        """
        Получает описание шага приготовления.
        
        Returns:
            str: Текстовое описание выполнения шага
        """
        return self.__description

    @description.setter
    def description(self, value: str):
        """
        Устанавливает описание шага приготовления с валидацией.
        
        Args:
            value (str): Описание шага приготовления
            
        Raises:
            ArgumentException: Если описание превышает максимальную длину
        """
        Validator.validate_argument(value, str, "description", max_length=500)
        self.__description = value.strip()

    def __str__(self) -> str:
        """
        Строковое представление шага приготовления.
        
        Returns:
            str: Шаг в формате "номер. описание"
        """
        return f"{self.step_number}. {self.description}"