class BaseException(Exception):
    """Базовое исключение для проекта"""
    pass

class ArgumentException(BaseException):
    """Исключение для ошибок аргументов"""
    pass

class OperationException(BaseException):
    """Исключение для ошибок операций"""
    pass


class Validator:

    @staticmethod
    def validate_argument(value, expected_type, argument_name="", max_length=None, min_length=None):
        """Валидация аргументов"""
        if value is None:
            raise ArgumentException(f"Аргумент '{argument_name}' не может быть None")
        
        if expected_type and not isinstance(value, expected_type):
            raise ArgumentException(f"Аргумент '{argument_name}' должен быть типа {expected_type.__name__}")
        
        if hasattr(value, '__len__') and min_length is not None and len(value) < min_length:
            raise ArgumentException(f"Аргумент '{argument_name}' должен содержать минимум {min_length} символов")
        
        if hasattr(value, '__len__') and max_length is not None and len(value) > max_length:
            raise ArgumentException(f"Аргумент '{argument_name}' должен содержать максимум {max_length} символов")