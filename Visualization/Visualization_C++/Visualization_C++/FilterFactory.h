#pragma once
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <queue>
#include <thread>
#include <queue>
#include <mutex>
#include <chrono>
#include <condition_variable>
#include <stdexcept>
#include "Filters.h"

using namespace std;
namespace py = pybind11;

enum class FilterType {
    TimeRange,
    Time,
    ThreadId,
    Cluster,
    Io,
    Quad,
    Unit,
    Area,
    Unknown,
};

class FilterFactory {
public:
    FilterFactory(string logsFileName);

    void addFilterToChain(pair<FilterType, Variant> filter);

    FilterType stringToFilterType(string str);

    void setStartTime(time_t time);

    void setEndTime(time_t time);

    void clearLogs();

    void startLogs();

    void joinThread();

    Generator<Log> getFilteredLogs();

    Log getLog();

    bool hasLog();

    void resetFilters();

    bool isFinishProcess();

    void removeFilter(FilterType filterToRemove);

    void removeLastFilter();

    void clearFilters();

    ~FilterFactory();

    std::mutex logMutex;
    std::condition_variable logCondition;

private:
    IViewPtr chain;
    shared_ptr<LogReader> logReader;
    LogsFactory logsFactory;
    bool isFinish;

    queue<Log> filteredLogs;
    std::thread filterThread;
    bool logAvailable = false;

    bool isTypeOfFilter(FilterType type, const shared_ptr<ILogFilter>& filter);

    IViewPtr createFilter(FilterType type, Variant& value);
};