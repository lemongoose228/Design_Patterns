from src.core.abstract_response import AbstractResponse


class ResponseMarkdown(AbstractResponse):
    """
    Класс для формирования Markdown ответов.
    """
    
    def build(self, data: list) -> str:
        """
        Формирует Markdown таблицу из данных.
        
        Args:
            data (list): Список объектов для конвертации
            
        Returns:
            str: Данные в формате Markdown таблицы
        """
        super().build(data)
        
        if len(data) == 0:
            return "Нет данных"
        
        # Получаем поля первого объекта
        first_item = data[0]
        fields = self._get_public_fields(first_item)
        
        # Формируем заголовок таблицы
        result = "| " + " | ".join(fields) + " |\n"
        result += "|" + "|".join(["---"] * len(fields)) + "|\n"
        
        # Формируем данные таблицы
        for item in data:
            row_data = []
            for field in fields:
                value = getattr(item, field, "")
                if value is None:
                    value = ""
                elif hasattr(value, 'name'):
                    value = getattr(value, 'name', str(value))
                row_data.append(str(value))
            result += "| " + " | ".join(row_data) + " |\n"
        
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
            if not attr_name.startswith('_') and not callable(getattr(obj, attr_name)):
                fields.append(attr_name)
        return sorted(fields)