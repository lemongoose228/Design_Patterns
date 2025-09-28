from src.models.company_model import CompanyModel

class Settings:
    __organization: CompanyModel = None

    def __init__(self):
        self.__organization = CompanyModel("Новая организация")

    @property
    def organization(self) -> CompanyModel:
        return self.__organization

    @organization.setter
    def organization(self, company_instance: CompanyModel):
        if isinstance(company_instance, CompanyModel):
            self.__organization = company_instance
        else:
            raise ValueError("Необходимо передать объект CompanyModel")