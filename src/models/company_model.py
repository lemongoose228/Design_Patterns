from src.core.abstract_model import AbstractModel


class CompanyModel(AbstractModel):
    __inn: str = ""
    __account: str = ""
    __correspondent_account: str = ""
    __BIK: str = ""
    __ownership_type: str = ""


    def __init__(self, name: str = ""):
        super().__init__(name)

    @property
    def inn(self) -> str:
        return self.__inn
    
    @inn.setter
    def inn(self, value: str|int) -> str:
        if isinstance(value, (str, int)):
            value = str(value)
            if len(value) == 12 and value.isdigit():
                self.__inn = value
            else:
                raise ValueError("ИНН должен содержать 12 цифр")
        else:
            raise ValueError("Поле должно быть строкой или числом")

    @property
    def account(self) -> str:
        return self.__account
    
    @account.setter
    def account(self, value: str|int) -> str:
        if isinstance(value, (str, int)):
            value = str(value)
            if len(value) == 11 and value.isdigit():
                self.__account = value
            else:
                raise ValueError("Счет должен содержать 11 цифр")
        else:
            raise ValueError("Поле должно быть строкой или числом")

    @property
    def correspondent_account(self) -> str:
        return self.__correspondent_account
    
    @correspondent_account.setter
    def correspondent_account(self, value: str|int) -> str:
        if isinstance(value, (str, int)):
            value = str(value)
            if len(value) == 11 and value.isdigit():
                self.__correspondent_account = value
            else:
                raise ValueError("Корреспондентский счет должен содержать 11 цифр")
        else:
            raise ValueError("Поле должно быть строкой или числом")
        
    @property
    def BIK(self) -> str:
        return self.__BIK
    
    @BIK.setter
    def BIK(self, value: str|int) -> str:
        if isinstance(value, (str, int)):
            value = str(value)
            if len(value) == 9 and value.isdigit():
                self.__BIK = value
            else:
                raise ValueError("БИК должен содержать 9 цифр")
        else:
            raise ValueError("Поле должно быть строкой или числом")

    @property
    def ownership_type(self) -> str:
        return self.__ownership_type
    
    @ownership_type.setter
    def ownership_type(self, value: str) -> str:
        if isinstance(value, str):
            if len(value) <= 5:
                self.__ownership_type = value
            else:
                raise ValueError("Вид собственности не более 5 символов")
        else:
            raise ValueError("Поле должно быть строкой или числом")