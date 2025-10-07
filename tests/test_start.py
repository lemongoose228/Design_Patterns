import unittest
from src.start_service import start_service
from src.models.receipt_model import ReceiptModel
from src.models.ingredient_model import IngredientModel
from src.models.cooking_step_model import CookingStepModel
from src.models.nomenclature_model import NomenclatureModel
from src.models.unit_model import UnitModel
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.core.validator import ArgumentException

class TestStartServiceData(unittest.TestCase):
    """
    Интеграционные тесты для сервиса создания данных
    """

    def setUp(self):
        """Настройка тестового окружения"""
        self.service = start_service()
        self.service.start()

    def test_ShouldCreateUnits_WhenServiceStarts_UnitsAreCreated(self):
        """Тест создания единиц измерения при запуске сервиса"""
        # Arrange
        units = self.service.data["range_model"]
        
        # Act & Assert
        self.assertGreater(len(units), 0, "Единицы измерения должны быть созданы")
        
        unit_names = [unit.name for unit in units]
        expected_units = ["грамм", "килограмм", "штука", "миллилитр", "литр", "столовая ложка", "чайная ложка", "щепотка"]
        
        for expected_unit in expected_units:
            with self.subTest(unit=expected_unit):
                self.assertIn(expected_unit, unit_names, f"Единица измерения '{expected_unit}' должна быть создана")

    def test_ShouldCreateGroups_WhenServiceStarts_GroupsAreCreated(self):
        """Тест создания номенклатурных групп при запуске сервиса"""
        # Arrange
        groups = self.service.data["nomenclature_group_model"]
        
        # Act & Assert
        self.assertGreater(len(groups), 0, "Номенклатурные группы должны быть созданы")
        
        group_names = [group.name for group in groups]
        expected_groups = ["Мучные изделия", "Овощи", "Молочные продукты"]
        
        for expected_group in expected_groups:
            with self.subTest(group=expected_group):
                self.assertIn(expected_group, group_names, f"Группа '{expected_group}' должна быть создана")

    def test_ShouldCreateNomenclature_WhenServiceStarts_NomenclatureIsCreated(self):
        """Тест создания номенклатуры при запуске сервиса"""
        # Arrange
        nomenclature = self.service.data["nomenclature_model"]
        
        # Act & Assert
        self.assertGreater(len(nomenclature), 0, "Номенклатура должна быть создана")
        
        nom_names = [nom.name for nom in nomenclature]
        expected_items = ["Мука пшеничная", "Картофель", "Яйца"]
        
        for expected_item in expected_items:
            with self.subTest(item=expected_item):
                self.assertIn(expected_item, nom_names, f"Номенклатура '{expected_item}' должна быть создана")

    def test_ShouldCreateReceipts_WhenCreateReceiptsCalled_ReceiptsAreCreated(self):
        """Тест создания рецептов при вызове метода create_receipts"""
        # Arrange & Act
        receipts = self.service.create_receipts()
        
        # Assert
        self.assertIsInstance(receipts, dict, "Рецепты должны возвращаться в виде словаря")
        self.assertGreater(len(receipts), 0, "Должен быть создан хотя бы один рецепт")
        
        receipt_names = list(receipts.keys())
        expected_receipts = ["Драники картофельные", "Салат витаминный с морковью и яблоком"]
        
        for expected_receipt in expected_receipts:
            with self.subTest(receipt=expected_receipt):
                self.assertIn(expected_receipt, receipt_names, f"Рецепт '{expected_receipt}' должен быть создан")

    def test_ShouldHaveCompleteReceiptStructure_WhenReceiptsCreated_StructureIsValid(self):
        """Тест структуры созданных рецептов"""
        # Arrange
        receipts = self.service.create_receipts()
        
        # Act & Assert
        for receipt_name, receipt_data in receipts.items():
            with self.subTest(receipt=receipt_name):
                self.assertIn("receipt", receipt_data, "Должен быть объект рецепта")
                self.assertIn("ingredients", receipt_data, "Должны быть ингредиенты")
                self.assertIn("steps", receipt_data, "Должны быть шаги приготовления")
                
                receipt = receipt_data["receipt"]
                ingredients = receipt_data["ingredients"]
                steps = receipt_data["steps"]
                
                self.assertIsInstance(receipt, ReceiptModel, "Объект рецепта должен быть экземпляром ReceiptModel")
                self.assertGreater(len(ingredients), 0, f"Рецепт '{receipt_name}' должен содержать ингредиенты")
                self.assertGreater(len(steps), 0, f"Рецепт '{receipt_name}' должен содержать шаги приготовления")

class TestIngredientModel(unittest.TestCase):
    """
    Юнит-тесты для модели ингредиента
    """

    def test_ShouldCreateIngredient_WhenValidParametersProvided_IngredientIsCreated(self):
        """Тест создания ингредиента с валидными параметрами"""
        # Arrange
        nomenclature = NomenclatureModel("Мука", "Мука пшеничная")
        unit = UnitModel("грамм", 1.0)
        
        # Act
        ingredient = IngredientModel(nomenclature, 100, unit)
        
        # Assert
        self.assertEqual(ingredient.nomenclature, nomenclature, "Номенклатура должна соответствовать установленной")
        self.assertEqual(ingredient.quantity, 100, "Количество должно соответствовать установленному")
        self.assertEqual(ingredient.unit, unit, "Единица измерения должна соответствовать установленной")

    def test_ShouldRaiseException_WhenInvalidNomenclatureProvided_ExceptionIsRaised(self):
        """Тест валидации номенклатуры ингредиента"""
        # Arrange
        unit = UnitModel("грамм", 1.0)
        
        # Act & Assert
        with self.assertRaises(ArgumentException):
            IngredientModel("invalid_nomenclature", 100, unit)

    def test_ShouldRaiseException_WhenInvalidQuantityProvided_ExceptionIsRaised(self):
        """Тест валидации количества ингредиента"""
        # Arrange
        nomenclature = NomenclatureModel("Мука", "Мука пшеничная")
        unit = UnitModel("грамм", 1.0)
        
        # Act & Assert
        with self.assertRaises(ArgumentException):
            IngredientModel(nomenclature, -100, unit)

    def test_ShouldRaiseException_WhenInvalidUnitProvided_ExceptionIsRaised(self):
        """Тест валидации единицы измерения ингредиента"""
        # Arrange
        nomenclature = NomenclatureModel("Мука", "Мука пшеничная")
        
        # Act & Assert
        with self.assertRaises(ArgumentException):
            IngredientModel(nomenclature, 100, "invalid_unit")

class TestCookingStepModel(unittest.TestCase):
    """
    Юнит-тесты для модели шага приготовления
    """

    def test_ShouldCreateCookingStep_WhenValidParametersProvided_StepIsCreated(self):
        """Тест создания шага приготовления с валидными параметрами"""
        # Arrange & Act
        step = CookingStepModel(1, "Подготовить ингредиенты")
        
        # Assert
        self.assertEqual(step.step_number, 1, "Номер шага должен соответствовать установленному")
        self.assertEqual(step.description, "Подготовить ингредиенты", "Описание должно соответствовать установленному")

    def test_ShouldRaiseException_WhenInvalidStepNumberProvided_ExceptionIsRaised(self):
        """Тест валидации номера шага приготовления"""
        # Act & Assert
        with self.assertRaises(ArgumentException):
            CookingStepModel(0, "Некорректный номер шага")

    def test_ShouldRaiseException_WhenInvalidDescriptionProvided_ExceptionIsRaised(self):
        """Тест валидации описания шага приготовления"""
        # Act & Assert
        with self.assertRaises(ArgumentException):
            CookingStepModel(1, "A" * 501)

class TestReceiptModel(unittest.TestCase):
    """
    Юнит-тесты для модели рецепта
    """

    def test_ShouldCreateReceipt_WhenValidParametersProvided_ReceiptIsCreated(self):
        """Тест создания рецепта с валидными параметрами"""
        # Arrange & Act
        receipt = ReceiptModel("Тестовый рецепт", 2, "20 мин")
        
        # Assert
        self.assertEqual(receipt.name, "Тестовый рецепт", "Название должно соответствовать установленному")
        self.assertEqual(receipt.portions, 2, "Количество порций должно соответствовать установленному")
        self.assertEqual(receipt.cooking_time, "20 мин", "Время приготовления должно соответствовать установленному")
        self.assertEqual(len(receipt.ingredients), 0, "Изначально не должно быть ингредиентов")
        self.assertEqual(len(receipt.cooking_steps), 0, "Изначально не должно быть шагов приготовления")

    def test_ShouldRaiseException_WhenInvalidPortionsProvided_ExceptionIsRaised(self):
        """Тест валидации количества порций рецепта"""
        # Act & Assert
        with self.assertRaises(ArgumentException):
            ReceiptModel("Тестовый рецепт", 0, "20 мин")

    def test_ShouldRaiseException_WhenInvalidCookingTimeProvided_ExceptionIsRaised(self):
        """Тест валидации времени приготовления рецепта"""
        # Act & Assert
        with self.assertRaises(ArgumentException):
            ReceiptModel("Тестовый рецепт", 2, "A" * 51)

if __name__ == '__main__':
    unittest.main()