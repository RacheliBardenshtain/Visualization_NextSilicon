import json
import time

from PyQt5.QtCore import pyqtSignal
import datetime
from entities.die import Die
from entities.host_interface import HostInterface
from utils.constants import *
from typing import Dict, Any, List, Union
from entities.log import Log
import filter_factory_module
import logs_factory

from entities.component import Component
from enum import Enum
from utils.filter_types import FILTER_TYPES, FILTER_TYPES_NAMES, CLUSTER
from utils.types_name import D2D, ECORE, EQ


class FilterType(Enum):
    TimeRange = 1
    Time = 2
    ThreadId = 3
    Cluster = 4
    Io = 5
    Quad = 6
    Unit = 7
    Area = 8
    Unknown = 9


class DataManager:
    def __init__(self, chip_file: str, sl_file: str, log_file: str):
        filter_changed = pyqtSignal(str, list)  # Signal to emit when filter changes

        self.chip_file = chip_file
        self.sl_file = sl_file
        self.log_file = log_file
        self.chip_data = self.load_json(self.chip_file)
        self.sl_data = self.load_json(self.sl_file)
        self.die_objects = {}
        self.die2die = Component(None, D2D)
        self.host_interface = self.load_host_interface()
        self.filter_factory = filter_factory_module.FilterFactory("data/logs.csv")
        self.logs_factory = logs_factory.LogsFactory('data/logs.csv')
        self.filter_types = filter_factory_module.FilterType

    def load_json(self, filename: str) -> Dict[str, Any]:
        try:
            with open(filename, 'r') as config:
                return json.load(config)
        except FileNotFoundError:
            print(f"Error: The file {filename} was not found.")
            return {}
        except json.JSONDecodeError:
            print(f"Error: The file {filename} is not a valid JSON.")
            return {}

    def load_die(self, die_index: int) -> Die:
        if die_index not in self.die_objects:
            die_data = self.chip_data.get(TOP, []).get(DIES, [])[die_index]
            self.die_objects[die_index] = Die(die_data[ID], die_data)
            if len(self.die_objects) == 2:
                self.enable_widgets()
                self.load_logs()

        return self.die_objects[die_index]

    def load_host_interface(self) -> HostInterface:
        host_interface_data = self.chip_data.get(TOP, {}).get(HOST_INTERFACE, {})
        self.host_interface = HostInterface(host_interface_data)
        return self.host_interface

    def load_logs(self):
        # self.change_start_and_end_time([self.logs_factory.get_first_log_time(),self.logs_factory.get_last_log_time()])
        self.link_the_logs_to_leaf_objects()

    def link_the_logs_to_leaf_objects(self):
        self.filter_factory.start_logs()

        while not self.filter_factory.is_finished_process() or self.filter_factory.has_log():
            if self.filter_factory.has_log():
                log = self.filter_factory.get_log()
                print("timestamp:", log.timeStamp
                      , " area:", log.area, ","
                      , " unit:", log.unit, ","
                      , " in/out:", log.io, ","
                      , " tid:", log.tid, ","
                      , " packet/data:", log.packet)
                self.link_the_log_to_leaf_object(log)

        self.filter_factory.join_thread()

    def link_the_log_to_leaf_object(self, log: Log) -> None:
        area = AREAS.get(log.area)
        unit = list(log.unit.split(";"))
        cluster_id = log.clusterId

        if self._is_bmt_or_pcie_area(area, cluster_id):
            self._add_log_to_host_interface(area, log)
        elif area == HOST_INTERFACE:
            self._add_log_to_host_interface_unit(unit, log)
        elif area == D2D:
            self.die2die.active_logs.append(log)
        else:
            self._add_log_to_die_area(area, unit, cluster_id, log)

    def _is_bmt_or_pcie_area(self, area, cluster_id) -> bool:
        return (area == BMT and cluster_id.row == -1) or area == PCIE

    def _add_log_to_host_interface(self, area, log: Log) -> None:
        getattr(self.host_interface, area).active_logs.append(log)

    def _add_log_to_host_interface_unit(self, unit, log: Log) -> None:
        current_eq = 0
        for detail in self.host_interface.get_all_inner_details():
            if detail.type_name == unit[0]:
                if detail.type_name == EQ:
                    current_eq += 1
                    if int(unit[1]) == current_eq:
                        detail.active_logs.append(log)
                        break
                else:
                    detail.active_logs.append(log)
                    break

    def _add_log_to_die_area(self, area, unit, cluster_id, log: Log) -> None:
        die = self.die_objects[cluster_id.die]
        quad = die.quads[cluster_id.quad // 2][cluster_id.quad % 2]
        if area == HBM:
            quad.hbm.active_logs.append(log)
        else:
            self._add_log_to_cluster(area, unit, quad, cluster_id, log)

    def _add_log_to_cluster(self, area, unit, quad, cluster_id, log: Log) -> None:
        cluster = quad.clusters[cluster_id.row][cluster_id.col]
        if area == MCU:
            self._add_log_to_mcu(unit, cluster, log)
        else:
            self._add_log_to_ecore_or_other(unit, cluster, log)

    def _add_log_to_mcu(self, unit, cluster, log: Log) -> None:
        current_eq = 0
        for detail in cluster.mcu.get_details():
            if detail.type_name == unit[0]:
                if detail.type_name == EQ:
                    current_eq += 1
                    if int(unit[1]) == current_eq:
                        detail.active_logs.append(log)
                        break
                else:
                    detail.active_logs.append(log)
                    break

    def _add_log_to_ecore_or_other(self, unit, cluster, log: Log) -> None:
        current_ecore = 0
        for detail in cluster.get_details():
            if detail.type_name == unit[0]:
                if detail.type_name == ECORE:
                    current_ecore += 1
                    if int(unit[1]) == current_ecore:
                        detail.active_logs.append(log)
                        break
                else:
                    detail.active_logs.append(log)
                    break

    def enable_widgets(self) -> None:
        for id in self.sl_data[ENABLED_CLUSTERS]:
            self.enable_widget_by_id(id[ID])
        self.enable_die()

    def enable_widget_by_id(self, id: Dict[str, int]) -> None:
        col, did, quad, row = id[COL], id[DID], id[QUAD], id[ROW]
        current_quad = self.die_objects[did].quads[quad // 2][quad % 2]
        current_quad.clusters[row][col].is_enable = True
        current_quad.is_enable = True

    def enable_die(self) -> None:
        for die_id, die in self.die_objects.items():
            for row in die.quads:
                for quad in row:
                    if quad and quad.is_enable:
                        die.is_enable = True
                        break
                if die.is_enable:
                    break

    def get_start_time(self) -> datetime:
        start_time = self.logs_factory.get_first_log_time()
        start_time_converted =datetime.datetime.fromtimestamp(start_time)
        print(start_time_converted)
        return start_time_converted

    def get_end_time(self) -> datetime:
        end_time = self.logs_factory.get_last_log_time()
        end_time_converted = datetime.datetime.fromtimestamp(end_time)  #here we need to convert the timestamp
        print(end_time_converted)
        return end_time_converted

    def change_filter(self, filter_type: str, values: List[Any]) -> None:
        # Changes the filter based on the filter name and values.
        if filter_type in FILTER_TYPES_NAMES.values():
            if filter_type == FILTER_TYPES_NAMES[CLUSTER]:
                cluster = filter_factory_module.Cluster(values[0], values[1], values[2], values[3], values[4])
                self.filter_factory.add_filter_to_chain((filter_type, cluster))
            else:
                self.filter_factory.add_filter_to_chain((filter_type, values))
            self.clean_the_prev_logs_from_leaf_objects()
            self.link_the_logs_to_leaf_objects()
        else:
            raise ValueError(f"Unknown filter: {filter_type}")

    def change_start_time(self,start_time):
        print(start_time)
        self.filter_factory.set_start_time(start_time)
        self.clean_the_prev_logs_from_leaf_objects()
        self.link_the_logs_to_leaf_objects()

    def change_end_time(self,end_time):
        print(end_time)
        self.filter_factory.set_end_time(end_time)
        self.clean_the_prev_logs_from_leaf_objects()
        self.link_the_logs_to_leaf_objects()

    def change_start_and_end_time(self,times):
        self.change_start_time(times[0])
        self.change_end_time(times[1])


    def clean_the_prev_logs_from_leaf_objects(self) -> None:
        # Cleaning the active logs in all leafs before connecting the new logs
        for die in self.die_objects.values():
            for quad_row in die.quads:
                for quad in quad_row:
                    quad.hbm.active_logs = []
                    for row in quad.clusters:
                        for cluster in row:
                            for detail in cluster.get_all_inner_details():
                                detail.active_logs = []

        for detail in self.host_interface.get_all_inner_details():
            detail.active_logs = []

        self.die2die.active_logs = []

    def clear_all_filters(self):
        self.filter_factory.clear_filters()
        self.clean_the_prev_logs_from_leaf_objects()
        self.link_the_logs_to_leaf_objects()

    def filter_removal(self, filter_type):
        self.filter_factory.remove_filter(filter_type)
        self.clean_the_prev_logs_from_leaf_objects()
        self.link_the_logs_to_leaf_objects()
