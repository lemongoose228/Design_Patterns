from src.core.abstract_response import AbstractResponse
from src.core.response_format import ResponseFormat
from src.core.validator import OperationException
from src.logics.response_csv import ResponseCSV
from src.logics.response_markdown import ResponseMarkdown
from src.logics.response_json import ResponseJSON
from src.logics.response_xml import ResponseXML
from src.settings_manager import SettingsManager


class FactoryEntities:
    """
    Фабрика для создания объектов формирования ответов в различных форматах.
    """
    
    def __init__(self):
        """Инициализирует фабрику с маппингом форматов."""
        self.__mapping = {
            ResponseFormat.CSV: ResponseCSV,
            ResponseFormat.MARKDOWN: ResponseMarkdown,
            ResponseFormat.JSON: ResponseJSON,
            ResponseFormat.XML: ResponseXML
        }
    
    def create(self, format_str: str) -> AbstractResponse:
        """
        Создает объект для формирования ответа в указанном формате.
        
        Args:
            format_str (str): Формат ответа
            
        Returns:
            AbstractResponse: Объект для формирования ответа
            
        Raises:
            OperationException: Если формат не поддерживается
        """
        if format_str not in self.__mapping:
            raise OperationException(f"Неподдерживаемый формат: {format_str}")
        
        response_class = self.__mapping[format_str]
        return response_class()
    
    def create_default(self) -> AbstractResponse:
        """
        Создает объект для формирования ответа в формате по умолчанию из настроек.
        
        Returns:
            AbstractResponse: Объект для формирования ответа
        """
        settings_manager = SettingsManager()
        default_format = settings_manager.app_config.response_format
        return self.create(default_format)
    
    def get_supported_formats(self) -> list:
        """
        Возвращает список поддерживаемых форматов.
        
        Returns:
            list: Список форматов
        """
        return list(self.__mapping.keys())