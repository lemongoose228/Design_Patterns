from src.models.company_model import CompanyModel
from src.core.response_format import ResponseFormat


class Settings:
    """
    Класс настроек приложения.
    """
    __organization: CompanyModel = None
    __response_format: str = ResponseFormat.JSON

    def __init__(self):
        """Инициализирует настройки значениями по умолчанию."""
        self.__organization = CompanyModel("Новая организация")
        self.__response_format = ResponseFormat.JSON

    @property
    def organization(self) -> CompanyModel:
        """
        Получает организацию.
        
        Returns:
            CompanyModel: Модель организации
        """
        return self.__organization

    @organization.setter
    def organization(self, company_instance: CompanyModel):
        """
        Устанавливает организацию.
        
        Args:
            company_instance (CompanyModel): Модель организации
            
        Raises:
            ValueError: Если передан неверный тип объекта
        """
        if isinstance(company_instance, CompanyModel):
            self.__organization = company_instance
        else:
            raise ValueError("Необходимо передать объект CompanyModel")

    @property
    def response_format(self) -> str:
        """
        Получает формат ответа по умолчанию.
        
        Returns:
            str: Формат ответа
        """
        return self.__response_format

    @response_format.setter
    def response_format(self, value: str):
        """
        Устанавливает формат ответа.
        
        Args:
            value (str): Формат ответа
            
        Raises:
            ValueError: Если формат не поддерживается
        """
        if value in ResponseFormat.get_all_formats():
            self.__response_format = value
        else:
            raise ValueError(f"Неподдерживаемый формат: {value}")