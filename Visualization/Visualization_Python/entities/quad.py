from utils.types_name import *
from entities.component import Component
from utils.constants import *
from entities.ecore import Ecore
from entities.cbu import Cbu
from entities.tcu import Tcu
from typing import Dict, Any, List, Union


class Quad(Component):
    def __init__(self, id: int, name: str, data: Dict[str, Any]):
        super().__init__(id, QUAD)
        self.name = name
        self.data = data
        self.clusters = [[None for _ in range(8)] for _ in range(8)]
        self.is_enable = False
        self.hbm = Component(None, HBM)

        self.init_clusters()

    # Initializing the clusters belonging to the quad and inserting them into the clusters matrix
    def init_clusters(self) -> None:
        self.init_ecore()
        self.init_cbus()
        self.init_tcus()

    # Initializing the ecore cluster
    def init_ecore(self) -> None:
        ecore_json = self.data[ECORE]
        cluster = self.init_cluster(ecore_json, ECORE)
        ecore = Ecore(cluster, ecore_json)
        self.clusters[int(ecore.row)][int(ecore.col)] = ecore

    # Initializing the cbu clusters
    def init_cbus(self) -> None:
        cbus = self.data.get(CBUS, [])
        for cbu_json in cbus:
            if not isinstance(cbu_json, dict):
                print(f"Warning: Invalid CBU data: {cbu_json}")
                continue
            cluster = self.init_cluster(cbu_json, CBU)
            cbu = Cbu(cluster, cbu_json)
            self.clusters[int(cbu.row)][int(cbu.col)] = cbu

    # Initializing the tcu clusters
    def init_tcus(self) -> None:
        tcus = self.data.get(TCUS, [])
        for tcu_json in tcus:
            if not isinstance(tcu_json, dict):
                print(f"Warning: Invalid TCU data: {tcu_json}")
                continue
            cluster = self.init_cluster(tcu_json, TCU)
            tcu = Tcu(cluster, tcu_json)
            self.clusters[int(tcu.row)][int(tcu.col)] = tcu

    # Initialize a cluster object according to its json object and type
    def init_cluster(self, cluster_json: Dict[str, Any], type: str) -> List[Union[int, str]]:
        cluster = [cluster_json.get(ROW),
                   cluster_json.get(COL),
                   cluster_json.get(CLUSTER_ID),
                   type]
        return cluster

    def get_attribute_from_active_logs(self,attribute):
        attributes=[]
        for row in self.clusters:
            for cluster in row:
                attributes.extend(cluster.get_attribute_from_active_logs(attribute))
        attributes.extend(super().get_attribute_from_active_logs(attribute))
        return attributes