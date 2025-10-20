from src.core.abstract_response import AbstractResponse
import xml.etree.ElementTree as ET


class ResponseXML(AbstractResponse):
    """
    Класс для формирования XML ответов.
    """
    
    def build(self, data: list) -> str:
        """
        Формирует XML строку из данных.
        
        Args:
            data (list): Список объектов для конвертации
            
        Returns:
            str: Данные в формате XML
        """
        super().build(data)
        
        if len(data) == 0:
            return '<?xml version="1.0" encoding="UTF-8"?><data></data>'
        
        # Определяем имя корневого элемента на основе типа данных
        root_name = self._get_root_name(data[0])
        root = ET.Element(root_name + "s")
        
        for item in data:
            item_element = ET.SubElement(root, root_name)
            self._add_object_to_xml(item_element, item)
        
        # Форматируем XML
        self._indent(root)
        return ET.tostring(root, encoding='unicode', method='xml')
    
    def _get_root_name(self, obj) -> str:
        """
        Определяет имя для корневого элемента на основе типа объекта.
        
        Args:
            obj: Объект для анализа
            
        Returns:
            str: Имя корневого элемента
        """
        class_name = obj.__class__.__name__.lower()
        if class_name.endswith('model'):
            return class_name[:-5]  # Убираем 'model'
        return class_name
    
    def _add_object_to_xml(self, parent_element, obj):
        """
        Добавляет объект в XML элемент.
        
        Args:
            parent_element: Родительский XML элемент
            obj: Объект для добавления
        """
        for attr_name in dir(obj):
            if not attr_name.startswith('_') and not callable(getattr(obj, attr_name)):
                value = getattr(obj, attr_name)
                if value is None:
                    value = ""
                elif hasattr(value, 'name'):
                    value = getattr(value, 'name', str(value))
                
                child = ET.SubElement(parent_element, attr_name)
                child.text = str(value)
    
    def _indent(self, elem, level=0):
        """
        Добавляет отступы для красивого форматирования XML.
        
        Args:
            elem: XML элемент
            level: Уровень вложенности
        """
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self._indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i