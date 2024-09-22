#include "LogReader.h"
#include <chrono>
#include <iomanip>

time_t LogReader::convertTimestamp(double timestamp) {
    return static_cast<time_t>(timestamp); 
}

Generator<Log> LogReader::getNext() {
    openFile();
    string line;
    Log log;
    time_t start;
    streampos position = logsFactory.binarySearchTimestamp(startTime);
    fileStream.seekg(position, ios::beg);

    getline(fileStream, line);
    start = logsFactory.extractTimestamp(line);
    if (start != startTime && startTime == endTime)
        co_return;

    while (!line.empty() && start <= endTime) {
        if (parseCSVLine(line, log)) {
            co_yield log;
        }

        getline(fileStream, line);

        if (!fileStream)
            break;

        start = logsFactory.extractTimestamp(line);
       
    }
    closeFile();
}

bool LogReader::parseCSVLine(const string& line, Log& log) {
    regex pattern(R"(timestamp:(\d+\.\d+)\s*,cluster_id:chip:(-?\d+);die:(-?\d+);quad:(-?\d+);row:(-?\d+);col:(-?\d+)\s*,area:(.*?),unit:(.*?),in/out:(in|out),tid:(\d+),packet/data:(.*))");
    smatch match;
    if (regex_match(line, match, pattern)) {
        try {
            double timestampDouble = stod(match[1]);
            log.timeStamp = convertTimestamp(timestampDouble);
        }
        catch (std::runtime_error e) {
            cerr << "Error parsing timestamp: " << e.what();
            return false;
        }
        log.clusterId.chip = stoi(match[2]);
        log.clusterId.die = stoi(match[3]);
        log.clusterId.quad = stoi(match[4]);
        log.clusterId.row = stoi(match[5]);
        log.clusterId.col = stoi(match[6]);
        log.area = match[7];
        log.unit = match[8];
        log.io = match[9] == "in" ? "in" : "out";
        log.tid = stoi(match[10]);
        log.packet = match[11];
        return true;
    }
    return false;
}

void LogReader::setStartTime(time_t start) {
    startTime = start;
}

void LogReader::setEndTime(time_t end) {
    endTime = end;
}

time_t LogReader::getStartTime() {
    return startTime;
}

time_t LogReader::getEndTime() {
    return endTime;
}

bool LogReader::isOpen() {
    return fileStream.is_open();
}

void LogReader::openFile() {
    if (!isOpen())
        fileStream.open(filePath);
    fileStream.seekg(0, ios::beg);
}

void LogReader::closeFile() {
    if (isOpen())
        fileStream.close();
}

