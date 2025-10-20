class ResponseFormat:
    """
    Статический класс с константами форматов ответов.
    """
    
    CSV = "csv"
    MARKDOWN = "markdown"
    JSON = "json"
    XML = "xml"
    
    @staticmethod
    def get_all_formats():
        """
        Возвращает список всех поддерживаемых форматов.
        
        Returns:
            list: Список форматов
        """
        return [ResponseFormat.CSV, ResponseFormat.MARKDOWN, ResponseFormat.JSON, ResponseFormat.XML]
    
    @staticmethod
    def is_valid_format(format_str: str) -> bool:
        """
        Проверяет валидность формата.
        
        Args:
            format_str (str): Проверяемый формат
            
        Returns:
            bool: True если формат валиден
        """
        return format_str in ResponseFormat.get_all_formats()