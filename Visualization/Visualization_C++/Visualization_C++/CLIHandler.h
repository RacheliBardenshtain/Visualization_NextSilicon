#ifndef CLIHANDLER_H
#define CLIHANDLER_H

//#include <CL/sycl.hpp>
#include "CLI11.hpp"
#include "FilterProcessor.h"
#include "CountProcessor.h"

//namespace std {
//	template <>
//	struct hash<pair<int, int>> {
//		size_t operator()(const pair<int, int>& p) const {
//			size_t h1 = hash<int>{}(p.first);
//			size_t h2 = hash<int>{}(p.second);
//			return h1 ^ (h2 << 1);
//		}
//	};
//}

using namespace std;
using namespace CLI;

class CLIHandler {
public:
	CLIHandler(int argc, char** argv);
	void execute();

private:
	CLI::App app;
	std::string inputFile = "logs.csv";
	std::string outputFile = "filtered_logs.csv";
	std::vector<std::string> filters;
	bool countFlag = false;

	void setupCLIOptions();
};

#endif
