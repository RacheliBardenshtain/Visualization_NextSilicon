#include "LogsGenerator.h"
#include "FilterFactory.h"
#include "PerformanceLogger.h"
#include "CLIHandler.h"
#include <thread>

using namespace std;
using namespace LogsGenerator;

int main(int argc, char** argv)
{
#pragma region GenerateLogFile
	// -----#  run only once  #------
	 //GenerateLogsFile("logs.csv");
#pragma endregion

	PerformanceLogger logger;

	if (argc > 1) {
		CLIHandler cliHandler(argc, argv);
		cliHandler.execute();
	}
	else {
		FilterFactory f("logs.csv");

		f.setStartTime(1726671491.525302);
		f.setEndTime(1726671531.525302);
		vector<int> vec = { 0,0,0 };
		f.addFilterToChain({ FilterType::Quad,vec });

		f.removeFilter(FilterType::Quad);

		f.startLogs();

		while (!f.isFinishProcess() || f.hasLog()) {
			if (f.hasLog()) {
				std::cout << f.getLog();
			}
		}

		f.joinThread();

		cout << "--------------------------------" << endl;

		f.addFilterToChain({ FilterType::Area,"cbu in mem1" });

		f.startLogs();

		while (!f.isFinishProcess() || f.hasLog()) {
			if (f.hasLog()) {
				std::cout << f.getLog();
			}
		}

		f.joinThread();

		cout << "--------------------------------" << endl;

		f.removeFilter(FilterType::Area);
		f.removeFilter(FilterType::Io);

		f.addFilterToChain({ FilterType::ThreadId,658 });

		f.startLogs();

		while (!f.isFinishProcess() || f.hasLog()) {
			if (f.hasLog()) {
				std::cout << f.getLog();
			}
		}

		f.joinThread();
		}
		return 0;
	}