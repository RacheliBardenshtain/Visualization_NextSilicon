#include "PerformanceLogger.h"

vector<string> filterFunctions;

PerformanceLogger::PerformanceLogger() {
	outputFile.open("run_metadata.txt", std::ios::app);
	if (!outputFile.is_open()) {
		std::cerr << "Error opening file for writing metadata." << std::endl;
	}
	start = high_resolution_clock::now();
}

PerformanceLogger::~PerformanceLogger() {
	end = high_resolution_clock::now();
	std::chrono::duration<double> duration = end - start;

	if (outputFile.is_open()) {
		outputFile << "Date: ";
		time_t now = system_clock::to_time_t(system_clock::now());
		tm* ltm = localtime(&now);
		outputFile << ltm->tm_hour << ":" << ltm->tm_min << ":" << ltm->tm_sec;
		outputFile << " " << ltm->tm_mday << "/" << 1 + ltm->tm_mon << "/" << 1900 + ltm->tm_year << endl;
		outputFile << "Duration: " << duration.count() << " seconds" << endl;
		outputFile << "Filter Functions: " << endl;
		for (auto& function : filterFunctions) {
			outputFile << function << endl;
		}
		outputFile << "------------------------------------------" << endl;
		outputFile.close();
	}
	else
		cerr << "Error writing metadata. File not open." << endl;
}