from utils.types_name import MCU
from entities.cluster import Cluster
from utils.constants import *
from typing import Dict, Any, List, Union
from entities.component import Component


class Cbu(Cluster):
    def __init__(self, cluster: List[Union[int, str]], data: Dict[str, Any]):
        mcu_data = data[MCU]
        super().__init__(cluster, mcu_data)
        self.data = data

    # The function returns the elements in the cbu and in the base cluster
    def get_details(self) -> List[Component]:
        return super().get_details()

    def get_all_inner_details(self) -> List[Component]:
        return super().get_all_inner_details()
