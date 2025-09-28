from src.models.settings import Settings
from src.models.company_model import CompanyModel
import json
import os

class SettingsManager:
    __config_file: str = ""
    __app_settings: Settings = None

    def __new__(cls, config_file: str = ""):
        if not hasattr(cls, '_instance'):
            cls._instance = super(SettingsManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, config_file: str = ""):
        if config_file:
            self.config_file = config_file
        if self.__app_settings is None:
            self.__app_settings = Settings()
            self.set_default_config()

    @property
    def app_config(self) -> Settings:
        return self.__app_settings

    @property
    def config_file(self) -> str:
        return self.__config_file

    @config_file.setter
    def config_file(self, file_path: str):
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
        """Преобразует данные конфигурации в объект Settings"""
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
            
        
        return settings

    def load_config(self) -> bool:
        """Загружает конфигурацию из файла"""
        if not self.__config_file or self.__config_file.strip() == "":
            raise FileNotFoundError("Не указан файл конфигурации")

        try:
            with open(self.__config_file, 'r', encoding='utf-8') as file:
                config_data = json.load(file)
                self.__app_settings = self.convert_config(config_data)
                return True
        except Exception as error:
            print(f"Ошибка загрузки конфигурации: {error}")
            return False

    def set_default_config(self):
        """Устанавливает конфигурацию по умолчанию"""
        default_company = CompanyModel("Ромашка")
        default_company.inn = "123456789012"
        default_company.account = "12345678901"
        default_company.correspondent_account = "12345678901"
        default_company.BIK = "123456789"
        default_company.ownership_type = "ООО"
        
        self.__app_settings.organization = default_company

    