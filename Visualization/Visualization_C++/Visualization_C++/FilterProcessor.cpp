#include "FilterProcessor.h"
#include <iostream>
#include <fstream>

FilterProcessor::FilterProcessor(const std::string& inputFile, const std::vector<std::string>& filters, const std::string& outputFile)
	: inputFile(inputFile), filters(filters), outputFile(outputFile) {}

void FilterProcessor::processFilters() {
	FilterFactory filterFactory(inputFile);
	applyFilters(filterFactory);

	std::ofstream outFile(outputFile);
	if (!outFile) {
		std::cerr << "Error opening output file: " << outputFile << std::endl;
		return;
	}

	std::cout << "Starting to write filtered logs..." << std::endl;
	int logCount = 0;

	for (auto log : filterFactory.getFilteredLogs()) {
		if (log.timeStamp > 0) {
			outFile << log;
			logCount++;
		}
	}

	cout << "Total logs written: " << logCount << std::endl;

	outFile.close();

	cout << "Filtering complete. Results saved to " << outputFile << std::endl;
}

void FilterProcessor::applyFilters(FilterFactory& filterFactory) {
	for (const auto& filter : filters) {
		size_t pos = filter.find('=');
		if (pos != string::npos) {
			string type = filter.substr(0, pos);
			string value = filter.substr(pos + 1);

			FilterType filterType = getFilterType(type);

			switch (filterType) {
			case FilterType::TimeRange: {
				size_t commaPos = value.find(',');
				if (commaPos != string::npos) {
					string startTimeStr = value.substr(0, commaPos);
					string endTimeStr = value.substr(commaPos + 1);

					try {
						double startTimeDouble = stod(startTimeStr);
						double endTimeDouble = stod(endTimeStr);

						time_t startTime = static_cast<time_t>(startTimeDouble);
						time_t endTime = static_cast<time_t>(endTimeDouble);

						filterFactory.setStartTime(startTime);
						filterFactory.setEndTime(endTime);
					}
					catch (const std::invalid_argument& e) {
						cerr << "Invalid TimeRange format. Could not parse time as a number." << std::endl;
					}
					catch (const std::out_of_range& e) {
						cerr << "Time value out of range." << std::endl;
					}
				}
				else {
					cerr << "Invalid TimeRange format. Expected 'TimeRange=start,end'" << std::endl;
				}
				break;
			}
			case FilterType::Time: {
				try {
					double timestampDouble = stod(value);

					time_t timestamp = static_cast<time_t>(timestampDouble);

					filterFactory.setStartTime(timestamp);
					filterFactory.setEndTime(timestamp);
				}
				catch (const std::invalid_argument& e) {
					cerr << "Invalid Time format. Could not parse time as a number." << std::endl;
				}
				catch (const std::out_of_range& e) {
					cerr << "Time value out of range." << std::endl;
				}
				break;
			}
			case FilterType::Cluster: {
				auto extractValue = [](const string& str) -> int {
					size_t colonPos = str.find(':');
					if (colonPos != string::npos) {
						return stoi(str.substr(colonPos + 1));
					}
					throw invalid_argument("Invalid format");
					};

				try {
					vector<string> parts;
					stringstream ss(value);
					string part;
					while (getline(ss, part, ',')) {
						parts.push_back(part);
					}

					if (parts.size() != 5) {
						throw invalid_argument("Invalid number of parameters");
					}
					int chip = extractValue(parts[0]);
					int die = extractValue(parts[1]);
					int quad = extractValue(parts[2]);
					int row = extractValue(parts[3]);
					int col = extractValue(parts[4]);

					filterFactory.addFilterToChain({ filterType, Cluster(chip, die, quad, row, col) });
				}
				catch (const std::exception& e) {
					cerr << "Invalid Cluster format. Expected 'Cluster=chip:<value>,die:<value>,quad:<value>,row:<value>,col:<value>'. Error: " << e.what() << std::endl;
				}
				break;
			}
			case FilterType::Io:
			case FilterType::Unit:
			case FilterType::Area:
				filterFactory.addFilterToChain({ filterType, value });
				break;
			case FilterType::Quad: {
				auto extractValue = [](const string& str) -> int {
					size_t colonPos = str.find(':');
					if (colonPos != string::npos) {
						return stoi(str.substr(colonPos + 1));
					}
					throw invalid_argument("Invalid format");
					};

				try {
					vector<string> parts;
					stringstream ss(value);
					string part;
					while (getline(ss, part, ',')) {
						parts.push_back(part);
					}

					if (parts.size() != 3) {
						throw invalid_argument("Invalid number of parameters");
					}

					int chip = extractValue(parts[0]);
					int die = extractValue(parts[1]);
					int quad = extractValue(parts[2]);

					filterFactory.addFilterToChain({ filterType, make_tuple(chip, die, quad) });
				}
				catch (const std::exception& e) {
					cerr << "Invalid Quad format. Expected 'Quad=Chip:<value>,Die:<value>,Quad:<value>'. Error: " << e.what() << std::endl;
				}
				break;
			}
			case FilterType::ThreadId: {
				try {
					vector<int> tids;
					stringstream ss(value);
					string tid;
					while (getline(ss, tid, ',')) {
						tids.push_back(stoi(tid));
					}
					if (!tids.empty()) {
						filterFactory.addFilterToChain({ filterType, tids });
					}
				}
				catch (const std::exception& e) {
					cerr << "Invalid ThreadId format. Expected 'ThreadId=value1,value2,...'. Error: " << e.what() << std::endl;
				}
				break;
			}
			default:
				cerr << "Unknown filter type: " << type << std::endl;
				break;
			}
		}
	}
}

void FilterProcessor::showFilterHelp() {
	cout << "Available filters and their expected formats:\n"
		<< "  TimeRange: TimeRange=start,end (e.g., ""TimeRange = 1726671491.525302, 1726671531.525302"")\n"
		<< "  Time: Time=value (e.g., Time=1723972947.9661083)\n"
		<< "  Quad: Quad=Chip:<value>,Die:<value>,Quad:<value> (e.g., Quad=Chip:0,Die:1,Quad:2)\n"
		<< "  ThreadId: ThreadId=value1,value2,... (e.g., ThreadId=7,10,15)\n"
		<< "  Unit: Unit=value (e.g., Unit=iqr)\n"
		<< "  Area: Area=value (e.g., Area=bmt)\n"
		<< "  Cluster: Cluster=chip:<value>,die:<value>,quad:<value>,row:<value>,col:<value> (e.g., Cluster=chip:0,die:1,quad:2,row:3,col:-1)\n"
		<< std::endl;
}

FilterType FilterProcessor::getFilterType(const string& type) {
	if (type == "TimeRange") return FilterType::TimeRange;
	else if (type == "Time") return FilterType::Time;
	else if (type == "Cluster") return FilterType::Cluster;
	else if (type == "Quad") return FilterType::Quad;
	else if (type == "ThreadId") return FilterType::ThreadId;
	else if (type == "Io") return FilterType::Io;
	else if (type == "Unit") return FilterType::Unit;
	else if (type == "Area") return FilterType::Area;
	return FilterType::Unknown;
}