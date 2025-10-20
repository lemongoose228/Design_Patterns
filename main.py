from src.start_service import start_service
from src.logics.factory_entities import FactoryEntities
from src.core.response_format import ResponseFormat
from src.settings_manager import SettingsManager
import os


def main():
    """
    Главная функция приложения.
    """
    print("=== Демонстрация работы с различными форматами вывода ===\n")
    
    # Инициализация сервиса
    service = start_service()
    service.start()
    
    # Инициализация фабрики
    factory = FactoryEntities()
    
    # Получение данных из репозитория
    repo_data = service.data
    
    # Демонстрация вывода в различных форматах
    data_types = [
        ("Единицы измерения", "range_model"),
        ("Номенклатурные группы", "nomenclature_group_model"),
        ("Номенклатура", "nomenclature_model")
    ]
    
    formats = ResponseFormat.get_all_formats()
    
    # Создаем директорию для результатов
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for data_type_name, data_key in data_types:
        print(f"\n--- {data_type_name} ---")
        
        data = repo_data.get(data_key, [])
        if not data:
            print(f"Нет данных для {data_type_name}")
            continue
        
        for format_str in formats:
            try:
                # Создаем объект формирования ответа
                response_object = factory.create(format_str)
                
                # Формируем ответ
                result = response_object.build(data)
                
                # Сохраняем в файл
                filename = f"{output_dir}/{data_type_name.replace(' ', '_').lower()}.{format_str}"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(result)
                
                print(f"  {format_str.upper()}: сохранено в {filename}")
                
                # Выводим небольшой превью
                preview = result[:200] + "..." if len(result) > 200 else result
                print(f"    Превью: {preview}")
                
            except Exception as e:
                print(f"  {format_str.upper()}: ошибка - {e}")
    
    # Демонстрация работы с рецептами
    print(f"\n--- Рецепты ---")
    receipts = service.create_receipts()
    
    for format_str in formats:
        try:
            # Для рецептов собираем все данные в один список
            receipt_data = []
            for receipt_name, receipt_info in receipts.items():
                receipt_data.append(receipt_info["receipt"])
            
            if receipt_data:
                response_object = factory.create(format_str)
                result = response_object.build(receipt_data)
                
                filename = f"{output_dir}/receipts.{format_str}"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(result)
                
                print(f"  {format_str.upper()}: сохранено в {filename}")
                
                preview = result[:200] + "..." if len(result) > 200 else result
                print(f"    Превью: {preview}")
            
        except Exception as e:
            print(f"  {format_str.upper()}: ошибка - {e}")
    
    # Демонстрация формата по умолчанию из настроек
    print(f"\n--- Формат по умолчанию из настроек ---")
    settings_manager = SettingsManager()
    default_format = settings_manager.app_config.response_format
    
    response_object = factory.create_default()
    units_data = repo_data.get("range_model", [])
    
    if units_data:
        result = response_object.build(units_data[:3])  # Первые 3 единицы измерения
        print(f"Формат по умолчанию: {default_format.upper()}")
        print(f"Пример вывода:\n{result}")
    
    print(f"\n=== Демонстрация завершена ===")
    print(f"Результаты сохранены в директорию: {output_dir}/")


if __name__ == "__main__":
    main()