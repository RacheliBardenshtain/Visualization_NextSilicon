from utils.types_name import *
from entities.component import Component
from utils.constants import *
from typing import List


class H2g(Component):
    def __init__(self, id: int, type: str):
        super().__init__(id, type)
        self.cbus_inj = Component(None, CBUS_INJ)
        self.cbus_clt = Component(None, CBUS_CLT)
        self.nfi_inj = Component(None, NFI_INJ)
        self.nfi_clt = Component(None, NFI_CLT)
        self.h2g_irqa = Component(None, IRQA)

    # The function returns the elements in the h2g
    def get_details(self) -> List[Component]:
        return [self.cbus_inj, self.cbus_clt, self.nfi_inj, self.nfi_clt, self.h2g_irqa]

    def get_attribute_from_active_logs(self, attribute):
        attributes = []
        for inner_obj in self.get_details():
            attributes.extend(inner_obj.get_attribute_from_active_logs(attribute))
        attributes.extend(super().get_attribute_from_active_logs(attribute))
        return attributes
