import unittest
from src.start_service import start_service
from src.models.receipt_model import ReceiptModel, IngredientModel, CookingStepModel
from src.models.nomenclature_model import NomenclatureModel
from src.models.unit_model import UnitModel
from src.models.nomenclature_group_model import NomenclatureGroupModel

class TestStartServiceData(unittest.TestCase):

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.service = start_service()
        self.service.start()

    def test_units_creation(self):
        """Тест создания единиц измерения"""
        units = self.service.data["range_model"]
        self.assertGreater(len(units), 0)
        
        unit_names = [unit.name for unit in units]
        self.assertIn("грамм", unit_names)
        self.assertIn("килограмм", unit_names)
        self.assertIn("штука", unit_names)

    def test_groups_creation(self):
        """Тест создания номенклатурных групп"""
        groups = self.service.data["nomenclature_group_model"]
        self.assertGreater(len(groups), 0)
        
        group_names = [group.name for group in groups]
        self.assertIn("Мучные изделия", group_names)
        self.assertIn("Овощи", group_names)
        self.assertIn("Молочные продукты", group_names)

    def test_nomenclature_creation(self):
        """Тест создания номенклатуры"""
        nomenclature = self.service.data["nomenclature_model"]
        self.assertGreater(len(nomenclature), 0)
        
        nom_names = [nom.name for nom in nomenclature]
        self.assertIn("Мука пшеничная", nom_names)
        self.assertIn("Картофель", nom_names)
        self.assertIn("Яйца", nom_names)

    def test_receipts_creation(self):
        """Тест создания рецептов"""
        receipts = self.service.create_receipts()
        self.assertGreater(len(receipts), 0)
        
        receipt_names = [receipt.name for receipt in receipts]
        self.assertIn("Драники картофельные", receipt_names)
        self.assertIn("Салат витаминный с морковью и яблоком", receipt_names)

    def test_receipt_structure(self):
        """Тест структуры рецептов"""
        receipts = self.service.create_receipts()
        
        for receipt in receipts:
            self.assertIsInstance(receipt, ReceiptModel)
            self.assertGreater(len(receipt.ingredients), 0)
            self.assertGreater(len(receipt.cooking_steps), 0)
            
            for ingredient in receipt.ingredients:
                self.assertIsInstance(ingredient, IngredientModel)
                self.assertIsInstance(ingredient.nomenclature, NomenclatureModel)
                self.assertIsInstance(ingredient.unit, UnitModel)
                self.assertGreater(ingredient.quantity, 0)
            
            for step in receipt.cooking_steps:
                self.assertIsInstance(step, CookingStepModel)
                self.assertGreater(len(step.description), 0)

class TestReceiptModels(unittest.TestCase):

    def test_ingredient_creation(self):
        """Тест создания ингредиента"""
        nomenclature = NomenclatureModel("Мука", "Мука пшеничная")
        unit = UnitModel("грамм", 1.0)
        
        ingredient = IngredientModel(nomenclature, 100, unit)
        
        self.assertEqual(ingredient.nomenclature, nomenclature)
        self.assertEqual(ingredient.quantity, 100)
        self.assertEqual(ingredient.unit, unit)

    def test_ingredient_validation(self):
        """Тест валидации ингредиента"""
        nomenclature = NomenclatureModel("Мука", "Мука пшеничная")
        unit = UnitModel("грамм", 1.0)
        
        with self.assertRaises(Exception):
            IngredientModel("invalid", 100, unit)
        
        with self.assertRaises(Exception):
            IngredientModel(nomenclature, -100, unit)
        
        with self.assertRaises(Exception):
            IngredientModel(nomenclature, 100, "invalid")

    def test_cooking_step_creation(self):
        """Тест создания шага приготовления"""
        step = CookingStepModel(1, "Подготовить ингредиенты")
        
        self.assertEqual(step.step_number, 1)
        self.assertEqual(step.description, "Подготовить ингредиенты")

    def test_cooking_step_validation(self):
        """Тест валидации шага приготовления"""
        with self.assertRaises(Exception):
            CookingStepModel(0, "Некорректный номер шага")
        
        with self.assertRaises(Exception):
            CookingStepModel(1, "A" * 501)  # Слишком длинное описание

    def test_receipt_creation(self):
        """Тест создания рецепта"""
        receipt = ReceiptModel("Тестовый рецепт", 2, "20 мин")
        
        self.assertEqual(receipt.name, "Тестовый рецепт")
        self.assertEqual(receipt.portions, 2)
        self.assertEqual(receipt.cooking_time, "20 мин")
        self.assertEqual(len(receipt.ingredients), 0)
        self.assertEqual(len(receipt.cooking_steps), 0)

    def test_receipt_add_ingredients_and_steps(self):
        """Тест добавления ингредиентов и шагов в рецепт"""
        receipt = ReceiptModel("Тестовый рецепт", 2, "20 мин")
        nomenclature = NomenclatureModel("Мука", "Мука пшеничная")
        unit = UnitModel("грамм", 1.0)
        
        ingredient = IngredientModel(nomenclature, 100, unit)
        step = CookingStepModel(1, "Подготовить ингредиенты")
        
        receipt.add_ingredient(ingredient)
        receipt.add_cooking_step(step)
        
        self.assertEqual(len(receipt.ingredients), 1)
        self.assertEqual(len(receipt.cooking_steps), 1)
        self.assertEqual(receipt.ingredients[0], ingredient)
        self.assertEqual(receipt.cooking_steps[0], step)

if __name__ == '__main__':
    unittest.main()