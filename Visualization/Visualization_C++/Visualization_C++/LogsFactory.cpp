#include "LogsFactory.h"
#include <iostream>

void LogsFactory::setPath(const string& path) {
	this->filePath = path;
}

time_t LogsFactory::getFirstLogTime() {
	openFile();
	fileStream.seekg(ios::beg);
	string timeStr = getTimeFromLine();
	return parseTimestamp(timeStr);
}

time_t LogsFactory::getLastLogTime() {
	openFile();

	fileStream.seekg(-3, ios::end);
	char ch;
	while (fileStream.tellg() > 1) {
		fileStream.get(ch);
		if (ch == '\n') {
			break;
		}
		fileStream.seekg(-2, std::ios::cur);
	}
	string timeStr = getTimeFromLine();
	return parseTimestamp(timeStr);
}

string LogsFactory::getTimeFromLine() {
	string line;
	string answer = "";

	if (getline(fileStream, line)) {
		regex pattern(R"(timestamp:(\d+\.\d+))");  
		smatch match;
		if (regex_search(line, match, pattern)) {
			try {
				answer = match[1];  
			}
			catch (runtime_error& e) {
				cerr << "Error parsing timestamp: " << e.what() << endl;
			}
		}
		else {
			cerr << "Timestamp not found in the log line." << endl;
		}
	}
	else {
		cerr << "Failed to read from file." << endl;
	}
	closeFile();
	return answer;
}

time_t LogsFactory::extractTimestamp(const string& line) {
	size_t pos = line.find("timestamp:");
	if (pos != string::npos) {
		string timestampStr = line.substr(pos + 10, 17);
		try {
			double timestampDouble = stod(timestampStr);
			return static_cast<time_t>(floor(timestampDouble));
		}
		catch (const std::invalid_argument& e) {
			cerr << "Invalid timestamp format: " << e.what() << endl;
			return -1;
		}
	}
	return -1;
}

string LogsFactory::time_tToString(time_t time) {
	struct tm* tm_info;
	tm_info = localtime(&time);
	char buffer[80];
	strftime(buffer, 80, "%d/%m/%Y %H:%M:%S", tm_info);
	return string(buffer);
}

time_t LogsFactory::parseTimestamp(const string& timestampStr) {
	try {
		double timestampDouble = stod(timestampStr); 
		return static_cast<time_t>(floor(timestampDouble));  
	}
	catch (const std::invalid_argument& e) {
		cerr << "Invalid timestamp format: " << e.what() << endl;
		return -1;
	}
}

streampos LogsFactory::binarySearchTimestamp(const time_t& targetTimestamp) {
	openFile();
	streampos left = 0;
	fileStream.seekg(0, std::ios::end);
	streampos right = fileStream.tellg();
	streampos result = -1;

	while (left <= right) {
		streamoff mid = left + (streamoff)((right - left) / 2);
		fileStream.seekg(mid);

		if (mid > 0) {
			std::string dummy;
			getline(fileStream, dummy);
		}

		streampos currentPos = fileStream.tellg();
		std::string line;
		getline(fileStream, line);

		if (line.empty()) {
			break;
		}

		time_t midTimestamp = extractTimestamp(line);

		if (compareTimestamps(midTimestamp, targetTimestamp) == 0) {
			result = currentPos;
			closeFile();
			return result;
		}
		else if (compareTimestamps(midTimestamp, targetTimestamp) > 0) {
			right = mid - 1;
		}
		else {
			result = currentPos;
			left = mid + 1;
		}
	}

	closeFile();
	return result;
}

int LogsFactory::compareTimestamps(time_t ts1, time_t ts2) {
	return (ts1 > ts2) - (ts1 < ts2);
}

void LogsFactory::openFile() {
	if (!fileStream.is_open())
		fileStream.open(filePath);
	fileStream.seekg(0, ios::beg);
}

void LogsFactory::closeFile() {
	if (fileStream.is_open())
		fileStream.close();
}

PYBIND11_MODULE(logs_factory, m) {
 m.doc() = "LogsFactory module: Provides functionality to read log timestamps from a file.";

 py::class_<LogsFactory>(m, "LogsFactory")
 .def(py::init<const std::string&>(), py::arg("path"), "Initialize LogsFactory with the given file path.")
 .def("get_first_log_time", &LogsFactory::getFirstLogTime, "Get the timestamp of the first log entry in the file.")
 .def("get_last_log_time", &LogsFactory::getLastLogTime, "Get the timestamp of the last log entry in the file.");
}
