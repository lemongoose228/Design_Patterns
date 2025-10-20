from src.models.settings import Settings
from src.models.company_model import CompanyModel
from src.core.response_format import ResponseFormat
import json
import os


class SettingsManager:
    """
    Менеджер настроек приложения.
    """
    __config_file: str = ""
    __app_settings: Settings = None

    def __new__(cls, config_file: str = ""):
        """
        Реализация синглтона.
        
        Args:
            config_file (str): Путь к файлу конфигурации
            
        Returns:
            SettingsManager: Экземпляр менеджера настроек
        """
        if not hasattr(cls, '_instance'):
            cls._instance = super(SettingsManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, config_file: str = ""):
        """
        Инициализирует менеджер настроек.
        
        Args:
            config_file (str): Путь к файлу конфигурации
        """
        if config_file:
            self.config_file = config_file
        if self.__app_settings is None:
            self.__app_settings = Settings()
            self.set_default_config()

    @property
    def app_config(self) -> Settings:
        """
        Получает текущие настройки приложения.
        
        Returns:
            Settings: Текущие настройки
        """
        return self.__app_settings

    @property
    def config_file(self) -> str:
        """
        Получает путь к файлу конфигурации.
        
        Returns:
            str: Путь к файлу конфигурации
        """
        return self.__config_file

    @config_file.setter
    def config_file(self, file_path: str):
        """
        Устанавливает путь к файлу конфигурации.
        
        Args:
            file_path (str): Путь к файлу конфигурации
            
        Raises:
            FileNotFoundError: Если файл не найден
        """
        if not file_path or file_path.strip() == "":
            return 
        
        if os.path.exists(file_path):
            self.__config_file = file_path.strip()
        else:
            # Поиск файла в любой директории
            for root, _, files in os.walk('.'):
                if os.path.basename(file_path) in files:
                    self.__config_file = os.path.join(root, os.path.basename(file_path))
                    return
            raise FileNotFoundError(f"Конфигурационный файл {file_path} не найден")

    def convert_config(self, config_data: dict) -> Settings:
        """
        Преобразует данные конфигурации в объект Settings.
        
        Args:
            config_data (dict): Данные конфигурации
            
        Returns:
            Settings: Объект настроек
        """
        settings = Settings()
        
        if "company" in config_data:
            company_info = config_data["company"]
            
            # Устанавливаем все свойства компании
            if "name" in company_info:
                settings.organization.name = company_info["name"]
            if "inn" in company_info:
                settings.organization.inn = company_info["inn"]
            if "account" in company_info:
                settings.organization.account = company_info["account"]
            if "correspondent_account" in company_info:
                settings.organization.correspondent_account = company_info["correspondent_account"]
            if "BIK" in company_info:
                settings.organization.BIK = company_info["BIK"]
            if "ownership_type" in company_info:
                settings.organization.ownership_type = company_info["ownership_type"]
        
        # Устанавливаем формат ответа
        if "response_format" in config_data:
            settings.response_format = config_data["response_format"]
        
        return settings

    def load_config(self) -> bool:
        """
        Загружает конфигурацию из файла.
        
        Returns:
            bool: True если загрузка успешна
            
        Raises:
            FileNotFoundError: Если файл конфигурации не указан
        """
        if not self.__config_file or self.__config_file.strip() == "":
            raise FileNotFoundError("Не указан файл конфигурации")

        try:
            with open(self.__config_file, 'r', encoding='utf-8') as file:
                config_data = json.load(file)
                self.__app_settings = self.convert_config(config_data)
                return True
        except Exception as error:
            raise Exception(f"Ошибка загрузки конфигурации: {error}")

    def set_default_config(self):
        """
        Устанавливает конфигурацию по умолчанию.
        """
        default_company = CompanyModel("Ромашка")
        default_company.inn = "123456789012"
        default_company.account = "12345678901"
        default_company.correspondent_account = "12345678901"
        default_company.BIK = "123456789"
        default_company.ownership_type = "ООО"
        
        self.__app_settings.organization = default_company
        self.__app_settings.response_format = ResponseFormat.JSON
    