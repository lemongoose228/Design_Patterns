from src.core.abstract_response import AbstractResponse
from src.core.validator import Validator


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
        
        # Используем фиксированный набор полей для разных типов объектов
        fields = self._determine_fields(data[0])
        
        # Формируем заголовок
        result = ";".join(fields) + "\n"
        
        # Формируем данные
        for item in data:
            row_data = []
            for field in fields:
                value = self._get_safe_value(item, field)
                # Экранируем точку с запятой и переносы строк
                value_str = str(value).replace(';', ',').replace('\n', ' ').replace('\r', '')
                row_data.append(value_str)
            result += ";".join(row_data) + "\n"
        
        return result
    
    def _determine_fields(self, obj) -> list:
        """
        Определяет поля для CSV на основе типа объекта.
        
        Args:
            obj: Объект для анализа
            
        Returns:
            list: Список полей
        """
        class_name = obj.__class__.__name__.lower()
        
        # Базовые поля для всех объектов
        base_fields = ['id', 'name']
        
        # Специфичные поля для разных типов объектов
        if 'unit' in class_name:
            return base_fields + ['factor']
        elif 'group' in class_name:
            return base_fields
        elif 'nomenclature' in class_name:
            return base_fields + ['full_name']
        elif 'receipt' in class_name:
            return base_fields + ['portions', 'cooking_time']
        elif 'company' in class_name:
            return base_fields + ['inn', 'ownership_type']
        else:
            # Для неизвестных типов используем безопасный подход
            return self._get_safe_fields(obj)
    
    def _get_safe_fields(self, obj) -> list:
        """
        Безопасно получает поля объекта.
        
        Args:
            obj: Объект для анализа
            
        Returns:
            list: Список безопасных полей
        """
        safe_fields = ['id', 'name']
        
        # Проверяем наличие стандартных полей
        for field in ['full_name', 'factor', 'portions', 'cooking_time', 'inn', 'ownership_type']:
            if hasattr(obj, field):
                safe_fields.append(field)
        
        return safe_fields
    
    def _get_safe_value(self, obj, field: str):
        """
        Безопасно получает значение поля.
        
        Args:
            obj: Объект
            field (str): Имя поля
            
        Returns:
            Значение поля
        """
        try:
            if not hasattr(obj, field):
                return ""
            
            value = getattr(obj, field)
            
            if value is None:
                return ""
            
            # Для вложенных объектов с полем name
            if hasattr(value, 'name') and not isinstance(value, (str, int, float)):
                return getattr(value, 'name', "")
            
            return value
            
        except Exception as e:
            return f"Error: {str(e)}"