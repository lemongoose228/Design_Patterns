import uuid
from src.settings_manager import SettingsManager
from src.models.company_model import CompanyModel
from src.models.settings import Settings
import unittest
from src.core.abstract_model import AbstractModel
from src.core.validator import ArgumentException
from src.models.storage_model import StorageModel
from src.models.unit_model import UnitModel
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.models.nomenclature_model import NomenclatureModel

class TestCompanyModel(unittest.TestCase):

    def test_create_empty_company(self):
        company = CompanyModel("ООО Япончикус Первый")
        self.assertEqual(company.name, "ООО Япончикус Первый")
        self.assertEqual(company.inn, "")
        self.assertEqual(company.account, "")
        self.assertEqual(company.correspondent_account, "")
        self.assertEqual(company.BIK, "")
        self.assertEqual(company.ownership_type, "")

    def test_company_all_properties_assignment(self):
        company = CompanyModel("Тестовая компания")
        
        # Устанавливаем все свойства

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
        company = CompanyModel("Тестовая компания")
        
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
        new_company = CompanyModel("Новая организация")
        
        # Устанавливаем все свойства
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

    # Проверка на сравнение двух по значению одинаковых моделей
    def test_equals_storage_model_create(self):
        # переопределить сравнение
        id = uuid.uuid4().hex
        storage1 = StorageModel("Склад хлеба")
        storage1.id = id
        storage2 = StorageModel("Склад хлеба2")
        storage2.id = id

        assert storage1 == storage2


class TestAbstractReference(unittest.TestCase):

    
    def test_creation(self):
        """Тест создания базовой модели"""
        model = AbstractModel("Тест")
        self.assertEqual(model.name, "Тест")
        self.assertIsNotNone(model.id)
    
    def test_name_validation(self):
        """Тест валидации наименования"""
        with self.assertRaises(ArgumentException):
            AbstractModel("")
        
        with self.assertRaises(ArgumentException):
            AbstractModel("A" * 51)
        
        # Корректное имя
        model = AbstractModel("A" * 50)
        self.assertEqual(len(model.name), 50)


class TestUnitModel(unittest.TestCase):
    
    def test_creation(self):
        """Тест создания единицы измерения"""
        unit = UnitModel("грамм", 1.0)
        self.assertEqual(unit.name, "грамм")
        self.assertEqual(unit.factor, 1.0)
        self.assertIsNone(unit.base_unit)

    def test_factor_validation(self):
        """Тест валидации коэффициента"""
        with self.assertRaises(ArgumentException):
            UnitModel("тест", 0)  # Нулевой коэффициент
        
        with self.assertRaises(ArgumentException):
            UnitModel("тест", -1)  # Отрицательный коэффициент


class TestNomenclatureModel(unittest.TestCase):
    
    def test_creation(self):
        """Тест создания номенклатуры"""
        group = NomenclatureGroupModel("Группа 1")
        unit = UnitModel("шт", 1.0)
        
        nomenclature = NomenclatureModel(
            name="Товар 1",
            full_name="Полное наименование товара 1",
            group=group,
            unit=unit
        )
        
        self.assertEqual(nomenclature.name, "Товар 1")
        self.assertEqual(nomenclature.full_name, "Полное наименование товара 1")
        self.assertEqual(nomenclature.group, group)
        self.assertEqual(nomenclature.unit, unit)
    
    def test_full_name_validation(self):
        """Тест валидации полного наименования"""
        # Корректная длина
        nomenclature = NomenclatureModel("Тест", "A" * 255)
        self.assertEqual(len(nomenclature.full_name), 255)
        
        # Слишком длинное наименование
        with self.assertRaises(ArgumentException):
            NomenclatureModel("Тест", "A" * 256)