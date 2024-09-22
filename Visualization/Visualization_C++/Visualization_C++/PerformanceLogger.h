#pragma once
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <chrono>

using namespace std;
using namespace std::chrono;

extern vector<string> filterFunctions;

class PerformanceLogger {
private:
	ofstream outputFile;
	high_resolution_clock::time_point start;
	high_resolution_clock::time_point end;

public:
	PerformanceLogger();

	~PerformanceLogger();
};
