#pragma once
#include <pybind11/pybind11.h>
#include <fstream>
#include <string>
#include <sstream>
#include <ctime>
#include <regex>
#include <iomanip>

using namespace std;
namespace py = pybind11;

class LogsFactory {
public:
	LogsFactory(const string& path) : filePath(path) {
	}

	LogsFactory() {
	}

	void setPath(const string& path);

	time_t getFirstLogTime();

	time_t getLastLogTime();

	time_t extractTimestamp(const string& line);

	string time_tToString(time_t time);

	time_t parseTimestamp(const string& timestampStr);

	streampos binarySearchTimestamp(const time_t& targetTimestamp);

	~LogsFactory() {
		fileStream.close();
	}
private:
	ifstream fileStream;
	string filePath;

	string getTimeFromLine();

	int compareTimestamps(time_t ts1, time_t ts2);

	void openFile();

	void closeFile();
};