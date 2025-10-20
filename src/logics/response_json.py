from src.core.abstract_response import AbstractResponse
import json


class ResponseJSON(AbstractResponse):
    """
    Класс для формирования JSON ответов.
    """
    
    def build(self, data: list) -> str:
        """
        Формирует JSON строку из данных.
        
        Args:
            data (list): Список объектов для конвертации
            
        Returns:
            str: Данные в формате JSON
        """
        super().build(data)
        
        # Конвертируем объекты в словари
        json_data = []
        for item in data:
            item_dict = self._object_to_dict(item)
            json_data.append(item_dict)
        
        return json.dumps(json_data, ensure_ascii=False, indent=2)
    
    def _object_to_dict(self, obj) -> dict:
        """
        Конвертирует объект в словарь.
        
        Args:
            obj: Объект для конвертации
            
        Returns:
            dict: Словарь с данными объекта
        """
        result = {}
        for attr_name in dir(obj):
            if not attr_name.startswith('_') and not callable(getattr(obj, attr_name)):
                value = getattr(obj, attr_name)
                # Рекурсивно обрабатываем вложенные объекты
                if hasattr(value, '__dict__') and not isinstance(value, (str, int, float, bool)):
                    value = self._object_to_dict(value)
                elif hasattr(value, 'name'):
                    value = getattr(value, 'name', str(value))
                result[attr_name] = value
        return result