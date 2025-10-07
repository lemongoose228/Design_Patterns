from src.reposity import reposity
from src.models.unit_model import UnitModel
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.models.nomenclature_model import NomenclatureModel
from src.models.receipt_model import ReceiptModel
from src.models.ingredient_model import IngredientModel
from src.models.cooking_step_model import CookingStepModel
from abc import ABC, abstractmethod

class BaseDataCreator(ABC):
    """Абстрактный класс с шаблонным методом для создания данных"""
    
    def create_data(self, repo: reposity):
        """Шаблонный метод"""
        self._create_units(repo)
        self._create_groups(repo)
        self._create_nomenclature(repo)
        self._create_receipts(repo)
    
    @abstractmethod
    def _create_units(self, repo: reposity):
        pass
    
    @abstractmethod
    def _create_groups(self, repo: reposity):
        pass
    
    @abstractmethod
    def _create_nomenclature(self, repo: reposity):
        pass
    
    @abstractmethod
    def _create_receipts(self, repo: reposity):
        pass

class DefaultDataCreator(BaseDataCreator):
    """Конкретная реализация создания данных по умолчанию"""
    
    def _create_units(self, repo: reposity):
        """Создание единиц измерения"""
        # Создаем уникальные базовые единицы
        gram_unit = UnitModel("грамм", 1.0)
        piece_unit = UnitModel("штука", 1.0)
        ml_unit = UnitModel("миллилитр", 1.0)
        
        # Создаем производные единицы с ссылками на базовые
        kg_unit = UnitModel("килограмм", 1000.0, gram_unit)
        liter_unit = UnitModel("литр", 1000.0, ml_unit)
        spoon_unit = UnitModel("столовая ложка", 15.0, gram_unit)
        tea_spoon_unit = UnitModel("чайная ложка", 5.0, gram_unit)
        pinch_unit = UnitModel("щепотка", 1.0, gram_unit)
        
        units = [
            gram_unit, kg_unit, piece_unit, ml_unit, liter_unit,
            spoon_unit, tea_spoon_unit, pinch_unit
        ]
        repo.set_data(reposity.range_key(), units)
    
    def _create_groups(self, repo: reposity):
        """Создание номенклатурных групп"""
        groups = [
            NomenclatureGroupModel("Мучные изделия"),
            NomenclatureGroupModel("Молочные продукты"),
            NomenclatureGroupModel("Овощи"),
            NomenclatureGroupModel("Фрукты"),
            NomenclatureGroupModel("Мясные продукты"),
            NomenclatureGroupModel("Специи и приправы"),
            NomenclatureGroupModel("Напитки")
        ]
        repo.set_data(reposity.nomenclature_group_key(), groups)
    
    def _create_nomenclature(self, repo: reposity):
        """Создание номенклатуры"""
        groups = repo.data.get(reposity.nomenclature_group_key(), [])
        units = repo.data.get(reposity.range_key(), [])
        
        # Находим нужные группы
        flour_group = self._find_or_create_group(groups, "Мучные изделия")
        veg_group = self._find_or_create_group(groups, "Овощи")
        milk_group = self._find_or_create_group(groups, "Молочные продукты")
        spice_group = self._find_or_create_group(groups, "Специи и приправы")
        fruit_group = self._find_or_create_group(groups, "Фрукты")
        
        # Находим нужные единицы измерения
        gram_unit = self._find_or_create_unit(units, "грамм", 1.0)
        piece_unit = self._find_or_create_unit(units, "штука", 1.0)
        spoon_unit = self._find_or_create_unit(units, "столовая ложка", 15.0)
        tea_spoon_unit = self._find_or_create_unit(units, "чайная ложка", 5.0)
        pinch_unit = self._find_or_create_unit(units, "щепотка", 1.0)
        
        nomenclature_list = [
            # Мучные изделия
            NomenclatureModel("Мука пшеничная", "Мука пшеничная высший сорт", flour_group, gram_unit),
            NomenclatureModel("Сахар", "Сахар белый кристаллический", spice_group, gram_unit),
            
            # Овощи
            NomenclatureModel("Картофель", "Картофель молодой", veg_group, piece_unit),
            NomenclatureModel("Лук репчатый", "Лук репчатый золотистый", veg_group, piece_unit),
            NomenclatureModel("Морковь", "Морковь столовая", veg_group, piece_unit),
            NomenclatureModel("Укроп", "Укроп свежий", veg_group, gram_unit),
            
            # Молочные продукты
            NomenclatureModel("Масло сливочное", "Масло сливочное 82,5%", milk_group, gram_unit),
            NomenclatureModel("Сметана", "Сметана 20%", milk_group, gram_unit),
            NomenclatureModel("Яйца", "Яйца куриные С0", milk_group, piece_unit),
            
            # Специи
            NomenclatureModel("Соль", "Соль поваренная", spice_group, tea_spoon_unit),
            NomenclatureModel("Перец черный", "Перец черный молотый", spice_group, pinch_unit),
            
            # Фрукты
            NomenclatureModel("Яблоки", "Яблоки зеленые", fruit_group, piece_unit),
        ]
        
        repo.set_data(reposity.nomenclature_key(), nomenclature_list)
    
    def _find_or_create_group(self, groups: list, group_name: str):
        """Находит группу по имени или создает новую"""
        for group in groups:
            if group.name == group_name:
                return group
        return NomenclatureGroupModel(group_name)
    
    def _find_or_create_unit(self, units: list, unit_name: str, factor: float = 1.0):
        """Находит единицу измерения по имени или создает новую"""
        for unit in units:
            if unit.name == unit_name:
                return unit
        return UnitModel(unit_name, factor)
    
    def _create_receipts(self, repo: reposity):
        """Создание рецептов"""
        nomenclature_list = repo.data.get(reposity.nomenclature_key(), [])
        units_list = repo.data.get(reposity.range_key(), [])
        
        # Создаем резервные объекты если что-то не найдено
        def find_nomenclature(name):
            for item in nomenclature_list:
                if item.name == name:
                    return item
            # Если не нашли, создаем новую номенклатуру
            return NomenclatureModel(name, name)
        
        def find_unit(name):
            for unit in units_list:
                if unit.name == name:
                    return unit
            # Если не нашли, создаем новую единицу
            return UnitModel(name, 1.0)
        
        # Рецепт 1: Драники картофельные
        драники = ReceiptModel("Драники картофельные", 4, "30 мин")
        
        # Ингредиенты для драников
        драники_ингредиенты = [
            IngredientModel(find_nomenclature("Картофель"), 500, find_unit("грамм")),
            IngredientModel(find_nomenclature("Лук репчатый"), 1, find_unit("штука")),
            IngredientModel(find_nomenclature("Яйца"), 1, find_unit("штука")),
            IngredientModel(find_nomenclature("Мука пшеничная"), 2, find_unit("столовая ложка")),
            IngredientModel(find_nomenclature("Соль"), 0.5, find_unit("чайная ложка")),
            IngredientModel(find_nomenclature("Перец черный"), 2, find_unit("щепотка")),
            IngredientModel(find_nomenclature("Масло сливочное"), 50, find_unit("грамм"))
        ]
        
        # Шаги приготовления драников
        драники_шаги = [
            CookingStepModel(1, "Картофель и лук очистить. Картофель натереть на мелкой терке, лук на мелкой терке или измельчить в блендере."),
            CookingStepModel(2, "Отжать лишнюю жидкость из картофельной массы. Добавить яйцо, муку, соль, перец. Тщательно перемешать."),
            CookingStepModel(3, "Разогреть сковороду с растительным маслом. Выкладывать тесто столовой ложкой, формируя оладьи."),
            CookingStepModel(4, "Жарить на среднем огне по 3-4 минуты с каждой стороны до золотистой корочки."),
            CookingStepModel(5, "Подавать горячими со сметаной.")
        ]
        
        # Рецепт 2: Салат витаминный
        салат = ReceiptModel("Салат витаминный с морковью и яблоком", 2, "15 мин")
        
        # Ингредиенты для салата
        салат_ингредиенты = [
            IngredientModel(find_nomenclature("Морковь"), 2, find_unit("штука")),
            IngredientModel(find_nomenclature("Яблоки"), 2, find_unit("штука")),
            IngredientModel(find_nomenclature("Сметана"), 100, find_unit("грамм")),
            IngredientModel(find_nomenclature("Сахар"), 1, find_unit("столовая ложка")),
            IngredientModel(find_nomenclature("Укроп"), 10, find_unit("грамм"))
        ]
        
        # Шаги приготовления салата
        салат_шаги = [
            CookingStepModel(1, "Морковь очистить и натереть на крупной терке."),
            CookingStepModel(2, "Яблоки вымыть, очистить от кожуры и сердцевины, натереть на крупной терке."),
            CookingStepModel(3, "Укроп мелко нарезать."),
            CookingStepModel(4, "Смешать морковь, яблоки и укроп в салатнице."),
            CookingStepModel(5, "Заправить сметаной, добавить сахар, аккуратно перемешать."),
            CookingStepModel(6, "Подавать сразу после приготовления.")
        ]
        
        # Сохраняем рецепты в репозиторий
        receipts_data = {
            "Драники картофельные": {
                "receipt": драники,
                "ingredients": драники_ингредиенты,
                "steps": драники_шаги
            },
            "Салат витаминный с морковью и яблоком": {
                "receipt": салат,
                "ingredients": салат_ингредиенты,
                "steps": салат_шаги
            }
        }
        
        repo.set_data(reposity.receipt_key(), receipts_data)

class start_service:
    __repo: reposity = None
    __data_creator: BaseDataCreator = None

    def __init__(self):
        self.__repo = reposity()
        self.__data_creator = DefaultDataCreator()

    # Singletone
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(start_service, cls).__new__(cls)
        return cls.instance 

    @property
    def data(self):
        return self.__repo.data   

    """
    Основной метод для генерации эталонных данных с использованием шаблонного метода
    """
    def start(self):
        self.__data_creator.create_data(self.__repo)

    """
    Фабричный метод для создания рецептов
    """
    def create_receipts(self):
        # Если рецепты еще не созданы, создаем их
        if not self.__repo.data.get(reposity.receipt_key()):
            self.__data_creator._create_receipts(self.__repo)
        return self.__repo.data[reposity.receipt_key()]