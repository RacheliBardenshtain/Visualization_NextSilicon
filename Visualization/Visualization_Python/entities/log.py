import  datetime

from entities.cluster_id import ClusterId


class Log():
    def __init__(self):
        self.time_t: datetime
        self.clusterId: ClusterId
        self.area: str
        self.unit: str
        self.io: int
        self.tid: str
        self.packet: str
        self.color: str