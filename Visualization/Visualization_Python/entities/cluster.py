from utils.types_name import *
from entities.component import Component
from entities.mcu import Mcu
from utils.constants import *
from typing import Dict, Any, List, Union


class Cluster(Component):
    def __init__(self, cluster: List[Union[int, str]], mcu_data: Dict[str, Any]):
        row, col, id, type_name = cluster
        super().__init__(id, type_name)
        self.row = row
        self.col = col
        self.color = OBJECT_COLORS[type_name]
        self.is_enable = False
        self.mcu = Mcu(None, MCU, mcu_data)
        self.lnb = Component(None, LNB)

    # The function returns the elements in the cluster
    def get_details(self) -> List[Component]:
        return [self.mcu, self.lnb]

    def get_all_inner_details(self) -> List[Component]:
        return [self.lnb, self.mcu] + self.mcu.get_details()

    def get_attribute_from_active_logs(self,attribute):
        attributes=[]
        for inner_obj in self.get_details():
            attributes.extend(inner_obj.get_attribute_from_active_logs(attribute))
        attributes.extend(super().get_attribute_from_active_logs(attribute))
        return attributes
