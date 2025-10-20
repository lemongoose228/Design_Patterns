"""
Демонстрационный скрипт для тестирования REST API.
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_endpoint(endpoint, format=None):
    """Тестирует эндпоинт API."""
    url = f"{BASE_URL}{endpoint}"
    if format:
        url += f"?format={format}"
    
    print(f"\n{'='*50}")
    print(f"Тестирование: {url}")
    print(f"{'='*50}")
    
    try:
        response = requests.get(url)
        print(f"Статус: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type')}")
        print(f"\nОтвет:")
        
        if 'json' in response.headers.get('content-type', ''):
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
            
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    print("Демонстрация REST API")
    
    # Тестируем различные эндпоинты и форматы
    test_endpoint("/api/formats")
    
    test_endpoint("/api/units") # JSON по умолчанию
    test_endpoint("/api/units", "markdown")
    test_endpoint("/api/units", "xml")
    
    test_endpoint("/api/groups", "json")
    test_endpoint("/api/nomenclature", "csv")
    test_endpoint("/api/receipts", "markdown")
    
    print(f"\n{'='*50}")
    print("Демонстрация завершена!")
    print(f"{'='*50}")