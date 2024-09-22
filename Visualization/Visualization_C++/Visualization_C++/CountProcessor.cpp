#include "CountProcessor.h"

CountProcessor::CountProcessor(const std::string& inputFile) : inputFile(inputFile) {}

void CountProcessor::processCounts() {
	string objectToCount;
	count();
	do {
		cout << "What do you want to count? (TID, UNIT, AREA, CLUSTER, QUAD): " << std::endl
			<< "To exit - enter Exit" << std::endl;
		cin >> objectToCount;
		if (objectToCount == "TID") {
			countTID();
		}
		else if (objectToCount == "UNIT") {
			countUNIT();
		}
		else if (objectToCount == "AREA") {
			countAREA();
		}
		else if (objectToCount == "CLUSTER") {
			countCLUSTER();
		}
		else if (objectToCount == "QUAD") {
			countQUAD();
		}
	} while (objectToCount != "Exit");
}

void CountProcessor::count() {
	PerformanceLogger p;
	LogReader logReader(inputFile);

	std::mutex countMutex;

	auto processLog = [&](const Log& log) {
		std::lock_guard<std::mutex> lock(countMutex);
		tidCount[log.tid]++;
		unitCount[log.unit]++;
		areaCount[log.area]++;
		clusterCount[log.clusterId]++;
		quadCount[make_pair(log.clusterId.die, log.clusterId.quad)]++;
		};

	std::vector<std::thread> workers;
	for (auto log : logReader.getNext()) {
		if (log.timeStamp > 0) {
			workers.emplace_back(processLog, log);
		}
	}

	for (auto& worker : workers) {
		worker.join();
	}
}

//void CountProcessor::count() {
//	PerformanceLogger p;
//	LogReader logReader(inputFile);
//
//	for (auto log : logReader.getNext())
//		if (log.timeStamp > 0) {
//			tidCount[log.tid]++;
//			unitCount[log.unit]++;
//			areaCount[log.area]++;
//			clusterCount[log.clusterId]++;
//			quadCount[make_pair(log.clusterId.die, log.clusterId.quad)]++;
//			cout << log.packet;
//		}
//}

void CountProcessor::countTID() {
	cout << "Counting TID..." << std::endl;
	cout << "Total TID: " << std::endl;

	for (const auto& [tid, count] : tidCount)
		cout << "TID: " << tid << " Count: " << count << std::endl;
}

void CountProcessor::countCLUSTER() {
	cout << "Counting CLUSTER..." << std::endl;
	cout << "Total CLUSTER: " << std::endl;

	for (const auto& [key, value] : clusterCount)
		cout << "Cluster: " << key << " Count: " << value << std::endl;
}

void CountProcessor::countUNIT() {
	cout << "Counting UNIT..." << std::endl;
	cout << "Total UNIT: " << std::endl;

	for (const auto& [key, value] : unitCount)
		cout << "Unit: " << key << " Count: " << value << std::endl;
}

void CountProcessor::countAREA() {
	cout << "Counting AREA..." << std::endl;
	cout << "Total AREA: " << std::endl;

	for (const auto& [key, value] : areaCount)
		cout << "Area: " << key << " Count: " << value << std::endl;
}

void CountProcessor::countQUAD() {
	cout << "Counting QUAD..." << std::endl;
	cout << "Total QUAD: " << std::endl;

	for (const auto& [key, value] : quadCount)
		cout << "Die: " << key.first << " Quad: " << key.second << " Count: " << value << std::endl;
}