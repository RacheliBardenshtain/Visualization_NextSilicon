#pragma once
#include <pybind11/pybind11.h>
#include <chrono>
#include <fstream>
#include <iomanip>
#include <random>
#include <stdexcept>
#include <string>
#include <vector>
#include "Cluster.h"

using namespace std;
namespace py = pybind11;

vector<string> areas = {
	"Nfi", "cbu in mem0", "cbu in mem1", "cbu in lcip", "mcu gate 0", "mcu gate 1", "ecore req", "ecore rsp", "pcie", "host_if", "bmt", "d2d", "hbm"
};

vector<string> units = {
	"BMT", "pcie", "cbus inj", "cbus clt", "nfi inj", "nfi clt", "iraq", "eq", "hbm", "tcu", "iqr", "iqd", "bin", "lnb"
};

namespace LogsGenerator {
    void GenerateLogsFile(const string& fileName) {
        ofstream file(fileName);
        if (!file.is_open()) {
            throw runtime_error("Failed to open file");
        }

        auto start = chrono::system_clock::now();
        auto startSec = chrono::duration_cast<chrono::duration<double>>(start.time_since_epoch()).count();

        for (int i = 0; i < 1000000; i++) {
            double entryTime = startSec + i;

            Cluster cluster_id;
            cluster_id.row = rand() % 8;
            cluster_id.col = rand() % 8;
            cluster_id.quad = rand() % 4;
            cluster_id.die = rand() % 2;
            cluster_id.chip = 0;

            int indexInAreaArray = rand() % areas.size();
            string nameArea = areas[indexInAreaArray];

            int indexInUnitArray = rand() % units.size();
            string nameUnit = units[indexInUnitArray];

            string io = (rand() % 2 == 0) ? "in" : "out";
            int tid = rand() % 1000;
            string data = "sample data " + to_string(i);

            file << fixed << setprecision(6)
                << "timestamp:" << entryTime << ","
                << "cluster_id:chip:" << cluster_id.chip << ";die:" << cluster_id.die << ";quad:" << cluster_id.quad << ";row:" << cluster_id.row << ";col:" << cluster_id.col << ","
                << "area:" << nameArea << ","
                << "unit:" << nameUnit << ","
                << "in/out:" << io << ","
                << "tid:" << tid << ","
                << "packet/data:" << data << "\n";
        }

        file.close();
    }
};