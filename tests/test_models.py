from src.settings_manager import SettingsManager
from src.models.company_model import CompanyModel
from src.models.settings import Settings
import unittest


class TestCompanyModel(unittest.TestCase):

    def test_create_empty_company(self):
        company = CompanyModel()
        self.assertEqual(company.name, "")
        self.assertEqual(company.inn, "")
        self.assertEqual(company.account, "")
        self.assertEqual(company.correspondent_account, "")
        self.assertEqual(company.BIK, "")
        self.assertEqual(company.ownership_type, "")

    def test_company_all_properties_assignment(self):
        company = CompanyModel()
        
        # Устанавливаем все свойства
        company.name = "Тестовая компания"
        company.inn = "123456789012"
        company.account = "12345678901"
        company.correspondent_account = "98765432109"
        company.BIK = "123456789"
        company.ownership_type = "ООО"
        
        # Проверяем все свойства
        self.assertEqual(company.name, "Тестовая компания")
        self.assertEqual(company.inn, "123456789012")
        self.assertEqual(company.account, "12345678901")
        self.assertEqual(company.correspondent_account, "98765432109")
        self.assertEqual(company.BIK, "123456789")
        self.assertEqual(company.ownership_type, "ООО")

    def test_company_data_validation(self):
        company = CompanyModel()
        
        # Проверка корректных данных
        company.inn = "123456789012"
        company.account = "12345678901"
        company.correspondent_account = "12345678901"
        company.BIK = "123456789"
        company.ownership_type = "ООО"
        
        self.assertEqual(company.inn, "123456789012")
        self.assertEqual(company.account, "12345678901")
        self.assertEqual(company.correspondent_account, "12345678901")
        self.assertEqual(company.BIK, "123456789")
        self.assertEqual(company.ownership_type, "ООО")
        
        # Проверка некорректных данных
        with self.assertRaises(ValueError):
            company.inn = "123"  
        with self.assertRaises(ValueError):
            company.account = "123"  
        with self.assertRaises(ValueError):
            company.correspondent_account = "123" 
        with self.assertRaises(ValueError):
            company.BIK = "123" 
        with self.assertRaises(ValueError):
            company.ownership_type = "ОАОАОАОАОАОАО слишком много символов"  

    def test_settings_initialization(self):
        settings = Settings()
        self.assertIsInstance(settings.organization, CompanyModel)

    def test_settings_all_properties(self):
        settings = Settings()
        new_company = CompanyModel()
        
        # Устанавливаем все свойства
        new_company.name = "Новая организация"
        new_company.inn = "987654321098"
        new_company.account = "98765432109"
        new_company.correspondent_account = "12345678901"
        new_company.BIK = "987654321"
        new_company.ownership_type = "ИП"
        
        settings.organization = new_company
        
        # Проверяем все свойства
        self.assertEqual(settings.organization.name, "Новая организация")
        self.assertEqual(settings.organization.inn, "987654321098")
        self.assertEqual(settings.organization.account, "98765432109")
        self.assertEqual(settings.organization.correspondent_account, "12345678901")
        self.assertEqual(settings.organization.BIK, "987654321")
        self.assertEqual(settings.organization.ownership_type, "ИП")

    def test_config_loading_all_properties(self):
        manager = SettingsManager("settings.json")
        success = manager.load_config()
        self.assertTrue(success)
        
        # Проверяем, что все свойства загрузились
        self.assertIsNotNone(manager.app_config.organization.name)
        self.assertIsNotNone(manager.app_config.organization.inn)
        self.assertIsNotNone(manager.app_config.organization.account)
        self.assertIsNotNone(manager.app_config.organization.correspondent_account)
        self.assertIsNotNone(manager.app_config.organization.BIK)
        self.assertIsNotNone(manager.app_config.organization.ownership_type)

    def test_config_conversion_all_properties(self):
        manager = SettingsManager()
        
        test_config = {
            "company": {
                "name": "Тестовая организация",
                "inn": "123456789012",
                "account": "12345678901",
                "correspondent_account": "98765432109",
                "BIK": "123456789",
                "ownership_type": "ООО"
            }
        }
        
        converted_settings = manager.convert_config(test_config)
        
        # Проверяем все свойства
        self.assertEqual(converted_settings.organization.name, "Тестовая организация")
        self.assertEqual(converted_settings.organization.inn, "123456789012")
        self.assertEqual(converted_settings.organization.account, "12345678901")
        self.assertEqual(converted_settings.organization.correspondent_account, "98765432109")
        self.assertEqual(converted_settings.organization.BIK, "123456789")
        self.assertEqual(converted_settings.organization.ownership_type, "ООО")

    def test_default_config_all_properties(self):
        manager = SettingsManager()
        manager.set_default_config()
        
        # Проверяем что все свойства по умолчанию установлены
        self.assertEqual(manager.app_config.organization.name, "Ромашка")
        self.assertEqual(manager.app_config.organization.inn, "123456789012")
        self.assertEqual(manager.app_config.organization.account, "12345678901")
        self.assertEqual(manager.app_config.organization.correspondent_account, "12345678901")
        self.assertEqual(manager.app_config.organization.BIK, "123456789")
        self.assertEqual(manager.app_config.organization.ownership_type, "ООО")