#pragma once
//#include <CL/sycl.hpp>
#include <vector>
#include <future>
#include <thread>
#include "IView.h"
#include "LogsFactory.h"

namespace std {
	template <>
	struct hash<pair<int, int>> {
		size_t operator()(const pair<int, int>& p) const {
			size_t h1 = hash<int>{}(p.first);
			size_t h2 = hash<int>{}(p.second);
			return h1 ^ (h2 << 1);
		}
	};
}

//using namespace sycl;

class LogReader : public IView {
public:
	LogReader(const string& path) : filePath(path) {
		logsFactory.setPath(path);
		openFile();
		startTime = logsFactory.getFirstLogTime();
		endTime = logsFactory.getLastLogTime();
	}

	LogReader() {}

	void openFile();

	void setPath(const string& path) {
		filePath = path;
		logsFactory.setPath(path);
		openFile();
		startTime = logsFactory.getFirstLogTime();
		endTime = logsFactory.getLastLogTime();
	}

	Generator<Log> getNext() override;

	size_t getFileSize() {
		openFile();
		fileStream.seekg(0, ios::end);
		size_t fileSize = fileStream.tellg();
		closeFile();
		return fileSize;
	}

	bool isOpen() override;

	time_t convertTimestamp(double timestamp);

	void setStartTime(time_t start);

	void setEndTime(time_t end);

	time_t getStartTime();

	time_t getEndTime();

	~LogReader() {
		fileStream.close();
	}

private:
	ifstream fileStream;
	string filePath;
	LogsFactory logsFactory;
	time_t startTime;
	time_t endTime;

	bool parseCSVLine(const string& line, Log& log);

	void closeFile();

#pragma region Try code on GPU
	//public:
	//	std::mutex map_mutex;
	//
	//	void processLogsOnGPU(std::vector<Log>& logs,
	//		std::unordered_map<int, int>& tidCount,
	//		std::unordered_map<std::string, int>& unitCount,
	//		std::unordered_map<std::string, int>& areaCount,
	//		std::unordered_map<Cluster, int>& clusterCount,
	//		std::unordered_map<std::pair<int, int>, int>& quadCount) {
	//		size_t logSize = logs.size();
	//
	//		queue q;
	//		{
	//			buffer<Log, 1> log_buffer(logs.data(), range<1>(logSize));
	//			buffer<int, 1> tid_count_buffer(logSize);
	//			buffer<int, 1> unit_count_buffer(logSize);
	//			buffer<int, 1> area_count_buffer(logSize);
	//			buffer<int, 1> cluster_count_buffer(logSize);
	//			buffer<int, 1> quad_count_buffer(logSize);
	//
	//			q.submit([&](handler& h) {
	//				auto log_acc = log_buffer.get_access<access::mode::read>(h);
	//				auto tid_count_acc = tid_count_buffer.get_access<access::mode::write>(h);
	//				auto unit_count_acc = unit_count_buffer.get_access<access::mode::write>(h);
	//				auto area_count_acc = area_count_buffer.get_access<access::mode::write>(h);
	//				auto cluster_count_acc = cluster_count_buffer.get_access<access::mode::write>(h);
	//				auto quad_count_acc = quad_count_buffer.get_access<access::mode::write>(h);
	//
	//				h.parallel_for(range<1>(logSize), [=](id<1> i) {
	//					auto log = log_acc[i];
	//					tid_count_acc[i] = 1;
	//					unit_count_acc[i] = 1;
	//					area_count_acc[i] = 1;
	//					cluster_count_acc[i] = 1;
	//					quad_count_acc[i] = 1;
	//					});
	//				}).wait();
	//
	//			auto tid_count_host = tid_count_buffer.get_access<access::mode::read>();
	//			auto unit_count_host = unit_count_buffer.get_access<access::mode::read>();
	//			auto area_count_host = area_count_buffer.get_access<access::mode::read>();
	//			auto cluster_count_host = cluster_count_buffer.get_access<access::mode::read>();
	//			auto quad_count_host = quad_count_buffer.get_access<access::mode::read>();
	//
	//			std::lock_guard<std::mutex> lock(map_mutex);
	//			for (size_t i = 0; i < logSize; ++i) {
	//				tidCount[logs[i].tid] += tid_count_host[i];
	//				unitCount[logs[i].unit] += unit_count_host[i];
	//				areaCount[logs[i].area] += area_count_host[i];
	//				clusterCount[logs[i].clusterId] += cluster_count_host[i];
	//				quadCount[std::make_pair(logs[i].clusterId.die, logs[i].clusterId.quad)] += quad_count_host[i];
	//			}
	//		}
	//	}
	//
	//	void getNextInParallel(size_t numThreads) {
	//		std::unordered_map<int, int> tidCount;
	//		std::unordered_map<std::string, int> unitCount;
	//		std::unordered_map<std::string, int> areaCount;
	//		std::unordered_map<Cluster, int> clusterCount;
	//		std::unordered_map<std::pair<int, int>, int> quadCount;
	//
	//		size_t fileSize = getFileSize();
	//		if (fileSize == 0) {
	//			std::cerr << "File size is 0 or file could not be opened." << std::endl;
	//			return;
	//		}
	//
	//		size_t chunkSize = fileSize / numThreads;
	//		std::vector<std::future<void>> futures;
	//
	//		for (size_t i = 0; i < numThreads; ++i) {
	//			futures.push_back(std::async(std::launch::async, [&, i]() {
	//				std::ifstream file(filePath);
	//				if (!file.is_open()) {
	//					std::cerr << "Error opening file." << std::endl;
	//					return;
	//				}
	//
	//				file.seekg(i * chunkSize);
	//				if (i > 0) {
	//					std::string dummy;
	//					std::getline(file, dummy);
	//				}
	//
	//				std::vector<Log> logs;
	//				std::string line;
	//				std::regex logRegex(R"(\d+)");
	//				std::smatch match;
	//
	//				while (file.tellg() < (i + 1 == numThreads ? fileSize : (i + 1) * chunkSize) && std::getline(file, line)) {
	//					Log log;
	//					logs.push_back(log);
	//				}
	//
	//				processLogsOnGPU(logs, tidCount, unitCount, areaCount, clusterCount, quadCount);
	//				}));
	//		}
	//
	//		for (auto& f : futures) {
	//			f.get();
	//		}
	//
	//		for (const auto& [key, value] : tidCount) {
	//			std::cout << "TID: " << key << " Count: " << value << std::endl;
	//		}
	//		for (const auto& [key, value] : unitCount) {
	//			std::cout << "Unit: " << key << " Count: " << value << std::endl;
	//		}
	//		for (const auto& [key, value] : areaCount) {
	//			std::cout << "Area: " << key << " Count: " << value << std::endl;
	//		}
	//		for (const auto& [key, value] : clusterCount) {
	//			std::cout << "Cluster: " << key << " Count: " << value << std::endl;
	//		}
	//		for (const auto& [key, value] : quadCount) {
	//			std::cout << "Quad: (" << key.first << ", " << key.second << ") Count: " << value << std::endl;
	//		}
	//	}

		//std::mutex map_mutex;
		/*vector<vector<Log>> getNextInParallel(size_t numThreads) {
			vector<vector<Log>> logBatches(numThreads);
			//size_t fileSize = getFileSize();

			//if (fileSize == 0) {
			//	cerr << "File size is 0 or file could not be opened." << std::endl;
				return logBatches;
			}

			size_t chunkSize = fileSize / numThreads;
			vector<future<void>> futures;

			for (size_t i = 0; i < numThreads; ++i) {
				futures.push_back(async(launch::async, [&, i]() {
					ifstream file(filePath);
					if (!file.is_open()) {
						cerr << "Error opening file in thread " << i << std::endl;
						return;
					}

					size_t startPos = i * chunkSize;
					file.seekg(startPos);

					if (startPos > 0) {
						string dummy;
						std::getline(file, dummy);
					}

					string line;
					Log log;

					while (file.tellg() < ((i + 1 == numThreads) ? fileSize : startPos + chunkSize) && std::getline(file, line)) {
						if (parseCSVLine(line, log)) {
							logBatches[i].push_back(log);
						}
					}
					}));
			}

			for (auto& f : futures) {
				f.get();
			}

			return logBatches;
		}*/
		/*void getNextInParallel(size_t numThreads) {
			unordered_map<int, int> countLogsMap;

			size_t fileSize = getFileSize();

			if (fileSize == 0) {
				cerr << "File size is 0 or file could not be opened." << std::endl;
				return;
			}

			size_t chunkSize = fileSize / numThreads;
			vector<future<void>> futures;

			for (size_t i = 0; i < numThreads; ++i) {
				futures.push_back(async(launch::async, [&, i]() {
					ifstream file(filePath);
					if (!file.is_open()) {
						cerr << "Error opening file in thread " << i << std::endl;
						return;
					}

					size_t startPos = i * chunkSize;
					file.seekg(startPos);

					if (startPos > 0) {
						string dummy;
						std::getline(file, dummy);
					}

					string line;
					Log log;

					while (file.tellg() < ((i + 1 == numThreads) ? fileSize : startPos + chunkSize) && std::getline(file, line)) {
						if (parseCSVLine(line, log)) {
							countLogsMap[log.tid] += 1;
						}
					}
					}));
			}

			for (auto& f : futures) {
				f.get();
			}

			for (const auto& [key, value] : countLogsMap) {
				cout << "TID: " << key << " Count: " << value << std::endl;
			}
		}*/
		/*unordered_map<int, int> getTIDCountInParallel(size_t numThreads) {
		unordered_map<int, int> countLogsMap;
		size_t fileSize = getFileSize();

		if (fileSize == 0) {
			cerr << "File size is 0 or file could not be opened." << std::endl;
			return countLogsMap;
		}

		size_t chunkSize = fileSize / numThreads;
		vector<future<void>> futures;

		for (size_t i = 0; i < numThreads; ++i) {
			futures.push_back(async(launch::async, [&, i]() {
				ifstream file(filePath);
				if (!file.is_open()) {
					cerr << "Error opening file in thread " << i << std::endl;
					return;
				}

				size_t startPos = i * chunkSize;
				file.seekg(startPos);

				if (startPos > 0) {
					string dummy;
					std::getline(file, dummy);
				}

				string line;
				Log log;

				while (file.tellg() < ((i + 1 == numThreads) ? fileSize : startPos + chunkSize) && std::getline(file, line)) {
					if (parseCSVLine(line, log)) {
						std::lock_guard<std::mutex> lock(map_mutex);
						countLogsMap[log.tid]++;
					}
				}
				}));
		}

		for (auto& f : futures) {
			f.get();
		}

		return countLogsMap;
		}*/

#pragma endregion

};
