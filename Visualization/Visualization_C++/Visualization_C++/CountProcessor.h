#ifndef COUNTPROCESSOR_H
#define COUNTPROCESSOR_H

#include <string>
#include <unordered_map>
#include <utility>
#include <iostream>
#include <thread>
#include <mutex>
//#include <CL/sycl.hpp>
#include "FilterFactory.h"

using namespace std;

class CountProcessor {
public:
    CountProcessor(const std::string& inputFile);
    void processCounts();

private:
    std::string inputFile;
	std::unordered_map<int, int> tidCount;
	std::unordered_map<std::string, int> unitCount;
	std::unordered_map<std::string, int> areaCount;
	std::unordered_map<Cluster, int> clusterCount;
	std::unordered_map<pair<int, int>, int> quadCount;

    void count();
    void countTID();
    void countUNIT();
    void countAREA();
    void countCLUSTER();
    void countQUAD();
};

#endif

#pragma region Try code
/*std::mutex map_mutex;
void processTIDOnGPU(vector<Log>& logs, unordered_map<int, int>& countLogsMap) {
	queue q;
	size_t logSize = logs.size();
	buffer<int, 1> tid_buffer(logSize);
	buffer<int, 1> count_buffer(logSize);

	{
		host_accessor tid_acc(tid_buffer, write_only);
		for (size_t i = 0; i < logSize; ++i) {
			tid_acc[i] = logs[i].tid;
		}
	}

	q.submit([&](handler& h) {
		accessor tid_acc(tid_buffer, h, read_only);
		accessor count_acc(count_buffer, h, write_only, no_init);

		h.parallel_for(range<1>(logSize), [=](id<1> i) {
			count_acc[i] = 1;
			});
		}).wait();

	host_accessor tid_acc(tid_buffer, read_only);
	host_accessor count_acc(count_buffer, read_only);
	std::lock_guard<std::mutex> lock(map_mutex);
	for (size_t i = 0; i < logSize; ++i) {
		countLogsMap[tid_acc[i]] += count_acc[i];
	}
}*/

//void countTID() {
//	//unordered_map<int, int> countLogsMap;
//	//vector<future<void>> futures;
//	LogReader logReader(inputFile);

//	cout << "Starting log processing..." << std::endl;
//	logReader.getNextInParallel(4);
//	//auto log_batches = logReader.getNextInParallel(4);

//	//if (log_batches.empty()) {
//	//	cerr << "No log batches were created. Check file path and file contents." << std::endl;
//	//	return;
//	//}

//	//cout << "Log batches obtained. Processing on GPU..." << std::endl;

//	//for (auto& logs : log_batches) {
//	//	futures.push_back(async(launch::async, [&]() {
//	//		processTIDOnGPU(logs, countLogsMap);
//	//		}));
//	//}

//	//for (auto& f : futures) {
//	//	f.get();
//	//}

//	//cout << "Log processing finished. Outputting results..." << std::endl;

//	//for (const auto& [key, value] : countLogsMap) {
//	//	cout << "TID: " << key << " Count: " << value << std::endl;
//	//}
//	//LogReader logReader("logs.csv");
//	//unordered_map<int, int> tidCountMap = logReader.getTIDCountInParallel(10); // לדוגמה, 4 threads

//	//for (const auto& [tid, count] : tidCountMap) {
//	//	cout << "TID: " << tid << " Count: " << count << std::endl;
//	//}
//}
#pragma endregion