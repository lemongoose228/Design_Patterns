from src.core.abstract_response import AbstractResponse
from src.core.validator import Validator
import inspect


class ResponseCSV(AbstractResponse):
    """
    Класс для формирования CSV ответов.
    """
    
    def build(self, data: list) -> str:
        """
        Формирует CSV строку из данных.
        
        Args:
            data (list): Список объектов для конвертации
            
        Returns:
            str: Данные в формате CSV
        """
        super().build(data)
        
        if len(data) == 0:
            return ""
        
        # Получаем поля первого объекта (исключая приватные и служебные)
        first_item = data[0]
        fields = self._get_public_fields(first_item)
        
        # Формируем заголовок
        result = ";".join(fields) + "\n"
        
        # Формируем данные
        for item in data:
            row_data = []
            for field in fields:
                value = getattr(item, field, "")
                # Преобразуем значения в строки
                if value is None:
                    value = ""
                elif hasattr(value, 'name'):
                    # Для объектов с полем name используем его
                    value = getattr(value, 'name', str(value))
                row_data.append(str(value))
            result += ";".join(row_data) + "\n"
        
        return result
    
    def _get_public_fields(self, obj) -> list:
        """
        Получает список публичных полей объекта.
        
        Args:
            obj: Объект для анализа
            
        Returns:
            list: Список публичных полей
        """
        fields = []
        for attr_name in dir(obj):
            # Исключаем приватные и служебные атрибуты
            if not attr_name.startswith('_') and not callable(getattr(obj, attr_name)):
                fields.append(attr_name)
        return sorted(fields)