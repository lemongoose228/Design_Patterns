import unittest
from src.logics.factory_entities import FactoryEntities
from src.core.response_format import ResponseFormat
from src.models.unit_model import UnitModel
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.models.nomenclature_model import NomenclatureModel
from src.core.abstract_response import AbstractResponse
from src.core.validator import OperationException


class TestResponseFormats(unittest.TestCase):
    """
    Тесты для проверки формирования ответов в различных форматах.
    """
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.factory = FactoryEntities()
        self.test_data = self._create_test_data()
    
    def _create_test_data(self):
        """Создает тестовые данные."""
        # Создаем тестовые единицы измерения
        gram_unit = UnitModel("грамм", 1.0)
        kg_unit = UnitModel("килограмм", 1000.0, gram_unit)
        
        # Создаем тестовые группы
        group1 = NomenclatureGroupModel("Мучные изделия")
        group2 = NomenclatureGroupModel("Овощи")
        
        # Создаем тестовую номенклатуру
        nomenclature1 = NomenclatureModel("Мука", "Мука пшеничная", group1, gram_unit)
        nomenclature2 = NomenclatureModel("Картофель", "Картофель молодой", group2, kg_unit)
        
        return [nomenclature1, nomenclature2]
    
    def test_ShouldCreateResponseObject_WhenValidFormatProvided_ObjectIsCreated(self):
        """Тест создания объектов формирования ответа для всех форматов."""
        formats = ResponseFormat.get_all_formats()
        
        for format_str in formats:
            with self.subTest(format=format_str):
                # Act
                response_object = self.factory.create(format_str)
                
                # Assert
                self.assertIsNotNone(response_object)
                self.assertIsInstance(response_object, AbstractResponse)
    
    def test_ShouldRaiseException_WhenInvalidFormatProvided_ExceptionIsRaised(self):
        """Тест исключения при неверном формате."""
        # Act & Assert
        with self.assertRaises(OperationException):
            self.factory.create("invalid_format")
    
    def test_ShouldCreateDefaultResponse_WhenCreateDefaultCalled_ObjectIsCreated(self):
        """Тест создания объекта формирования ответа по умолчанию."""
        # Act
        response_object = self.factory.create_default()
        
        # Assert
        self.assertIsNotNone(response_object)
        self.assertIsInstance(response_object, AbstractResponse)
    
    def test_ShouldGenerateCSV_WhenValidDataProvided_CSVIsGenerated(self):
        """Тест генерации CSV формата."""
        # Arrange
        csv_response = self.factory.create(ResponseFormat.CSV)
        
        # Act
        result = csv_response.build(self.test_data)
        
        # Assert
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
        self.assertIn("name;", result)  # Проверяем заголовок
        self.assertIn("Мука;", result)  # Проверяем данные
    
    def test_ShouldGenerateMarkdown_WhenValidDataProvided_MarkdownIsGenerated(self):
        """Тест генерации Markdown формата."""
        # Arrange
        md_response = self.factory.create(ResponseFormat.MARKDOWN)
        
        # Act
        result = md_response.build(self.test_data)
        
        # Assert
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
        self.assertIn("| name |", result)  # Проверяем заголовок
        self.assertIn("| Мука |", result)  # Проверяем данные
    
    def test_ShouldGenerateJSON_WhenValidDataProvided_JSONIsGenerated(self):
        """Тест генерации JSON формата."""
        # Arrange
        json_response = self.factory.create(ResponseFormat.JSON)
        
        # Act
        result = json_response.build(self.test_data)
        
        # Assert
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
        self.assertIn('"name": "Мука"', result)  # Проверяем данные
    
    def test_ShouldGenerateXML_WhenValidDataProvided_XMLIsGenerated(self):
        """Тест генерации XML формата."""
        # Arrange
        xml_response = self.factory.create(ResponseFormat.XML)
        
        # Act
        result = xml_response.build(self.test_data)
        
        # Assert
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
        self.assertIn("<name>Мука</name>", result)  # Проверяем данные
    
    def test_ShouldRaiseException_WhenEmptyDataProvided_ExceptionIsRaised(self):
        """Тест исключения при пустых данных."""
        # Arrange
        empty_data = []
        csv_response = self.factory.create(ResponseFormat.CSV)
        
        # Act & Assert
        with self.assertRaises(OperationException):
            csv_response.build(empty_data)
    
    def test_ShouldReturnSupportedFormats_WhenGetSupportedFormatsCalled_FormatsAreReturned(self):
        """Тест получения списка поддерживаемых форматов."""
        # Act
        formats = self.factory.get_supported_formats()
        
        # Assert
        self.assertIsInstance(formats, list)
        self.assertGreater(len(formats), 0)
        self.assertIn(ResponseFormat.CSV, formats)
        self.assertIn(ResponseFormat.MARKDOWN, formats)
        self.assertIn(ResponseFormat.JSON, formats)
        self.assertIn(ResponseFormat.XML, formats)


class TestSettingsResponseFormat(unittest.TestCase):
    """
    Тесты для проверки настроек формата ответа.
    """
    
    def test_ShouldSetResponseFormat_WhenValidFormatProvided_FormatIsSet(self):
        """Тест установки формата ответа в настройках."""
        # Arrange
        from src.settings_manager import SettingsManager
        manager = SettingsManager()
        
        # Act
        manager.app_config.response_format = ResponseFormat.MARKDOWN
        
        # Assert
        self.assertEqual(manager.app_config.response_format, ResponseFormat.MARKDOWN)
    
    def test_ShouldRaiseException_WhenInvalidFormatProvided_ExceptionIsRaised(self):
        """Тест исключения при неверном формате в настройках."""
        # Arrange
        from src.settings_manager import SettingsManager
        manager = SettingsManager()
        
        # Act & Assert
        with self.assertRaises(ValueError):
            manager.app_config.response_format = "invalid_format"


if __name__ == '__main__':
    unittest.main()