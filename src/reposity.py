"""
Репозиторий данных
"""
class reposity:
    __data = {}

    def __init__(self):
        # Инициализируем данные при создании экземпляра
        self.__data = {
            self.range_key(): [],
            self.nomenclature_group_key(): [],
            self.nomenclature_key(): [],
            self.receipt_key(): []
        }

    @property
    def data(self):
        return self.__data
    
    @data.setter
    def data(self, value: dict):
        """Сеттер для установки всех данных репозитория"""
        if not isinstance(value, dict):
            raise ValueError("Данные должны быть словарем")
        self.__data = value
    
    def set_data(self, key: str, value):
        """Установка данных по ключу"""
        self.__data[key] = value
    
    """
    Ключ для единиц измерений
    """
    @staticmethod
    def range_key():
        return "range_model"

    """
    Ключ для номенклатурных групп
    """
    @staticmethod
    def nomenclature_group_key():
        return "nomenclature_group_model"

    """
    Ключ для номенклатуры
    """
    @staticmethod
    def nomenclature_key():
        return "nomenclature_model"

    """
    Ключ для рецептов
    """
    @staticmethod
    def receipt_key():
        return "receipt_model"