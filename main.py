import os
import sys
from typing import List, Tuple

from src.start_service import start_service
from src.logics.factory_entities import FactoryEntities
from src.core.response_format import ResponseFormat
from src.settings_manager import SettingsManager
from src.core.validator import OperationException


class ExportResult:
    """Результат операции экспорта."""
    
    def __init__(self, success: bool, message: str = "", files: List[str] = None):
        self.success = success
        self.message = message
        self.files = files or []
    
    def __bool__(self):
        return self.success


def log_info(message: str):
    """Логирует информационное сообщение."""
    sys.stdout.write(f"ℹ️  {message}\n")
    sys.stdout.flush()


def log_success(message: str):
    """Логирует сообщение об успехе."""
    sys.stdout.write(f"✅ {message}\n")
    sys.stdout.flush()


def log_warning(message: str):
    """Логирует предупреждение."""
    sys.stderr.write(f"⚠️  {message}\n")
    sys.stderr.flush()


def log_error(message: str):
    """Логирует сообщение об ошибке."""
    sys.stderr.write(f"❌ {message}\n")
    sys.stderr.flush()


def ensure_output_dir(output_dir: str) -> bool:
    """
    Создает директорию для результатов если она не существует.
    
    Args:
        output_dir (str): Путь к директории
        
    Returns:
        bool: True если директория готова к использованию
    """
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            log_info(f"Создана директория: {output_dir}")
        return True
    except Exception as e:
        log_error(f"Ошибка создания директории {output_dir}: {e}")
        return False


def export_data_to_format(data: List, data_type: str, format_str: str, 
                         output_dir: str, factory: FactoryEntities) -> ExportResult:
    """
    Экспортирует данные в указанном формате.
    
    Args:
        data: Данные для экспорта
        data_type: Тип данных (для имени файла)
        format_str: Формат экспорта
        output_dir: Директория для сохранения
        factory: Фабрика для создания форматеров
        
    Returns:
        ExportResult: Результат операции
    """
    try:
        if not data:
            return ExportResult(False, f"Нет данных для экспорта {data_type}")
        
        # Создаем объект формирования ответа
        formatter = factory.create(format_str)
        
        # Формируем ответ
        result = formatter.build(data)
        
        if not result:
            return ExportResult(False, f"Пустой результат для {data_type} в {format_str}")
        
        # Сохраняем в файл
        filename = f"{data_type.lower().replace(' ', '_')}.{format_str}"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(result)
        
        return ExportResult(True, f"Экспортирован {data_type} в {format_str}", [filepath])
        
    except OperationException as e:
        return ExportResult(False, f"Ошибка формата {format_str} для {data_type}: {e}")
    except IOError as e:
        return ExportResult(False, f"Ошибка записи файла {format_str} для {data_type}: {e}")
    except Exception as e:
        return ExportResult(False, f"Неожиданная ошибка при экспорте {data_type} в {format_str}: {e}")


def export_all_data_types(service, factory: FactoryEntities, output_dir: str) -> bool:
    """
    Экспортирует все основные типы данных во всех форматах.
    
    Args:
        service: Сервис с данными
        factory: Фабрика форматеров
        output_dir: Директория для сохранения
        
    Returns:
        bool: True если все экспорты успешны
    """
    data_types = [
        ("Единицы измерения", "range_model"),
        ("Номенклатурные группы", "nomenclature_group_model"), 
        ("Номенклатура", "nomenclature_model")
    ]
    
    formats = ResponseFormat.get_all_formats()
    all_success = True
    
    for data_type_name, data_key in data_types:
        log_info(f"Экспорт {data_type_name}...")
        
        data = service.data.get(data_key, [])
        if not data:
            log_warning(f"Пропуск {data_type_name}: нет данных")
            continue
        
        type_success = True
        for format_str in formats:
            result = export_data_to_format(data, data_type_name, format_str, output_dir, factory)
            
            if result:
                log_success(result.message)
            else:
                log_error(result.message)
                type_success = False
                all_success = False
        
        if type_success:
            log_success(f"Все форматы {data_type_name} экспортированы успешно")
    
    return all_success


def export_receipts(service, factory: FactoryEntities, output_dir: str) -> bool:
    """
    Экспортирует рецепты во всех форматах.
    
    Args:
        service: Сервис с данными
        factory: Фабрика форматеров
        output_dir: Директория для сохранения
        
    Returns:
        bool: True если экспорт успешен
    """
    log_info("Экспорт рецептов...")
    
    try:
        receipts = service.create_receipts()
        if not receipts:
            log_warning("Пропуск рецептов: нет данных")
            return True
        
        # Собираем объекты рецептов
        receipt_objects = [receipt_info["receipt"] for receipt_info in receipts.values()]
        
        formats = ResponseFormat.get_all_formats()
        all_success = True
        
        for format_str in formats:
            result = export_data_to_format(receipt_objects, "receipts", format_str, output_dir, factory)
            
            if result:
                log_success(result.message)
            else:
                log_error(result.message)
                all_success = False
        
        return all_success
        
    except Exception as e:
        log_error(f"Ошибка экспорта рецептов: {e}")
        return False


def demonstrate_default_format(service, factory: FactoryEntities, settings_manager: SettingsManager):
    """
    Демонстрирует работу формата по умолчанию.
    
    Args:
        service: Сервис с данными
        factory: Фабрика форматеров
        settings_manager: Менеджер настроек
    """
    try:
        default_format = settings_manager.app_config.response_format
        log_info(f"Формат по умолчанию: {default_format.upper()}")
        
        formatter = factory.create_default()
        units_data = service.data.get("range_model", [])
        
        if units_data:
            # Берем только первые 2 записи для демонстрации
            demo_data = units_data[:2]
            result = formatter.build(demo_data)
            
            log_info("Пример вывода:")
            for line in result.split('\n')[:5]:  # Показываем первые 5 строк
                if line.strip():
                    sys.stdout.write(f"  {line}\n")
            sys.stdout.flush()
        else:
            log_warning("Нет данных для демонстрации")
            
    except Exception as e:
        log_error(f"Ошибка демонстрации формата по умолчанию: {e}")


def main() -> int:
    """
    Главная функция приложения.
    
    Returns:
        int: Код возврата (0 - успех, 1 - ошибка)
    """
    try:
        log_info("=== Демонстрация работы с различными форматами вывода ===")
        
        # Инициализация сервисов
        log_info("Инициализация сервисов...")
        service = start_service()
        service.start()
        
        factory = FactoryEntities()
        settings_manager = SettingsManager()
        log_success("Сервисы инициализированы")
        
        # Подготовка директории
        output_dir = "output"
        if not ensure_output_dir(output_dir):
            return 1
        
        # Экспорт данных
        success = export_all_data_types(service, factory, output_dir)
        success = export_receipts(service, factory, output_dir) and success
        
        # Демонстрация формата по умолчанию
        demonstrate_default_format(service, factory, settings_manager)
        
        # Итог
        if success:
            log_success("=== Все данные успешно экспортированы ===")
            log_info(f"Результаты в директории: {output_dir}/")
            return 0
        else:
            log_warning("=== Экспорт завершен с ошибками ===")
            log_info(f"Частичные результаты в директории: {output_dir}/")
            return 1
            
    except KeyboardInterrupt:
        log_info("Программа прервана пользователем")
        return 130
    except Exception as e:
        log_error(f"Критическая ошибка: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)