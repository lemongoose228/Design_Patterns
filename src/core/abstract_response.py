import abc
from src.core.validator import Validator, OperationException


class AbstractResponse(abc.ABC):
    """
    Абстрактный класс для формирования ответов в различных форматах.
    """
    
    @abc.abstractmethod
    def build(self, data: list) -> str:
        """
        Формирует ответ в нужном формате.
        
        Args:
            data (list): Данные для форматирования
            
        Returns:
            str: Данные в требуемом формате
            
        Raises:
            OperationException: Если данные пусты
        """
        Validator.validate_argument(data, list, "data")
        
        if len(data) == 0:
            raise OperationException("Нет данных для форматирования!")
        
        return ""