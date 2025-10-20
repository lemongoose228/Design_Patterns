"""
сервер для демонстрации работы с различными форматами вывода.
"""
from flask import Flask, jsonify, request, Response
from src.start_service import start_service
from src.logics.factory_entities import FactoryEntities
from src.core.response_format import ResponseFormat
from src.settings_manager import SettingsManager
import json

app = Flask(__name__)

# Инициализация сервисов
service = start_service()
service.start()
factory = FactoryEntities()

@app.route('/')
def index():
    """Главная страница API."""
    return """
    <h1>REST API Демонстрация</h1>
    <h2>Доступные эндпоинты:</h2>
    <ul>
        <li><a href="/api/units">/api/units</a> - Единицы измерения</li>
        <li><a href="/api/groups">/api/groups</a> - Номенклатурные группы</li>
        <li><a href="/api/nomenclature">/api/nomenclature</a> - Номенклатура</li>
        <li><a href="/api/receipts">/api/receipts</a> - Рецепты</li>
        <li><a href="/api/formats">/api/formats</a> - Поддерживаемые форматы</li>
    </ul>
    <h3>Использование:</h3>
    <p>Добавьте параметр ?format= к URL для выбора формата (csv, markdown, json, xml)</p>
    <p>Пример: /api/units?format=csv</p>
    """

@app.route('/api/formats')
def get_formats():
    """Возвращает список поддерживаемых форматов."""
    formats = factory.get_supported_formats()
    return jsonify({
        "supported_formats": formats,
        "default_format": SettingsManager().app_config.response_format
    })

@app.route('/api/units')
def get_units():
    """Возвращает единицы измерения в указанном формате."""
    format_str = request.args.get('format', SettingsManager().app_config.response_format)
    return _get_data_in_format('range_model', format_str, "Единицы измерения")

@app.route('/api/groups')
def get_groups():
    """Возвращает номенклатурные группы в указанном формате."""
    format_str = request.args.get('format', SettingsManager().app_config.response_format)
    return _get_data_in_format('nomenclature_group_model', format_str, "Номенклатурные группы")

@app.route('/api/nomenclature')
def get_nomenclature():
    """Возвращает номенклатуру в указанном формате."""
    format_str = request.args.get('format', SettingsManager().app_config.response_format)
    return _get_data_in_format('nomenclature_model', format_str, "Номенклатура")

@app.route('/api/receipts')
def get_receipts():
    """Возвращает рецепты в указанном формате."""
    format_str = request.args.get('format', SettingsManager().app_config.response_format)
    
    try:
        receipts_data = service.create_receipts()
        receipt_objects = [receipt_info["receipt"] for receipt_info in receipts_data.values()]
        
        response_object = factory.create(format_str)
        result = response_object.build(receipt_objects)
        
        return _create_response(result, format_str, "Рецепты")
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def _get_data_in_format(data_key, format_str, data_name):
    """
    Вспомогательная функция для получения данных в указанном формате.
    
    Args:
        data_key: Ключ данных в репозитории
        format_str: Формат вывода
        data_name: Название данных для заголовков
    
    Returns:
        Response: HTTP ответ с данными в указанном формате
    """
    try:
        data = service.data.get(data_key, [])
        if not data:
            return jsonify({"error": f"Нет данных для {data_name}"}), 404
        
        response_object = factory.create(format_str)
        result = response_object.build(data)
        
        return _create_response(result, format_str, data_name)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def _create_response(data, format_str, data_name):
    """
    Создает HTTP ответ с правильными заголовками.
    
    Args:
        data: Данные для отправки
        format_str: Формат данных
        data_name: Название данных
    
    Returns:
        Response: HTTP ответ
    """
    content_types = {
        ResponseFormat.CSV: 'text/csv',
        ResponseFormat.MARKDOWN: 'text/markdown',
        ResponseFormat.JSON: 'application/json',
        ResponseFormat.XML: 'application/xml'
    }
    
    content_type = content_types.get(format_str, 'text/plain')
    
    if format_str == ResponseFormat.CSV:
        filename = f"{data_name.lower().replace(' ', '_')}.csv"
        return Response(
            data,
            mimetype=content_type,
            headers={'Content-Disposition': f'attachment; filename={filename}'}
        )
    elif format_str == ResponseFormat.MARKDOWN:
        return Response(data, mimetype=content_type)
    elif format_str == ResponseFormat.JSON:
        return Response(data, mimetype=content_type)
    elif format_str == ResponseFormat.XML:
        return Response(data, mimetype=content_type)
    else:
        return Response(data, mimetype='text/plain')

if __name__ == '__main__':
    print("Запуск REST API сервера...")
    print("Доступные эндпоинты:")
    print("  http://localhost:5000/")
    print("  http://localhost:5000/api/units")
    print("  http://localhost:5000/api/groups") 
    print("  http://localhost:5000/api/nomenclature")
    print("  http://localhost:5000/api/receipts")
    print("  http://localhost:5000/api/formats")
    print("\nИспользуйте параметр ?format=csv|markdown|json|xml для выбора формата")
    
    app.run(debug=True, host='0.0.0.0', port=5000)