#include "FilterFactory.h"
#include <memory>

namespace py = pybind11;

FilterFactory::FilterFactory(string logsFileName) {
	isFinish = false;
	chain = logReader = make_shared<LogReader>(logsFileName);
}

void FilterFactory::addFilterToChain(pair<FilterType, Variant> filter) {
	chain = createFilter(filter.first, filter.second);
}

FilterType FilterFactory::stringToFilterType(string str) {
	if (str == "TimeRange") return FilterType::TimeRange;
	if (str == "Time") return FilterType::Time;
	if (str == "ThreadId") return FilterType::ThreadId;
	if (str == "Cluster") return FilterType::Cluster;
	if (str == "Io") return FilterType::Io;
	if (str == "Quad") return FilterType::Quad;
	if (str == "Unit") return FilterType::Unit;
	if (str == "Area") return FilterType::Area;
	return FilterType::Unknown;
}

void FilterFactory::setStartTime(time_t time) {
	logReader->setStartTime(time);
}

void FilterFactory::setEndTime(time_t time) {
	logReader->setEndTime(time);
}

Generator<Log> FilterFactory::getFilteredLogs() {
	return chain->getNext();
}

bool FilterFactory::isFinishProcess() {
	return isFinish;
}

void FilterFactory::resetFilters() {
	logReader->openFile();
}

void FilterFactory::clearLogs() {
	std::lock_guard<std::mutex> lock(logMutex);
	std::queue<Log> emptyQueue;
	std::swap(filteredLogs, emptyQueue);
}

void FilterFactory::startLogs() {
	resetFilters();
	clearLogs();
	isFinish = false;
	if (filterThread.joinable()) {
		filterThread.join();
	}
	try {
		filterThread = std::thread([this]() {
			for (auto log : chain->getNext()) {
				if (log.timeStamp > 0) {
					{
						std::lock_guard<std::mutex> lock(logMutex);
						filteredLogs.push(log);
					}
					logCondition.notify_one();
				}
			}
			isFinish = true;
			});
	}
	catch (...) {
		std::cerr << "Thread creation failed." << std::endl;
	}
}

void FilterFactory::joinThread() {
	if (filterThread.joinable()) {
		filterThread.join();
		filterThread = std::thread();
	}
}

Log FilterFactory::getLog() {
	std::lock_guard<std::mutex> lock(logMutex);
	if (!filteredLogs.empty()) {
		Log log = filteredLogs.front();
		filteredLogs.pop();
		return log;
	}
	throw std::runtime_error("No logs available");
}

bool FilterFactory::hasLog() {
	std::lock_guard<std::mutex> lock(logMutex);
	return !filteredLogs.empty();
}

void FilterFactory::removeFilter(FilterType filterToRemove) {
	IViewPtr current = chain;
	IViewPtr prev = nullptr;
	while (current) {
		if (auto filter = dynamic_pointer_cast<ILogFilter>(current)) {
			if (isTypeOfFilter(filterToRemove, filter)) {
				if (prev) {
					if (auto prevFilter = dynamic_pointer_cast<ILogFilter>(prev)) {
						prevFilter->base = filter->base;
					}
				}
				else {
					chain = filter->base;
				}
				return;
			}
			prev = current;
			current = filter->base;
		}
		else {
			break;
		}
	}
}

void FilterFactory::removeLastFilter() {
	IViewPtr filterToRemove = chain;
	if (auto filter = dynamic_pointer_cast<ILogFilter>(filterToRemove)) {
		chain = dynamic_pointer_cast<ILogFilter>(filterToRemove)->base;
	}
}

void FilterFactory::clearFilters() {
	chain = logReader;
	filterFunctions.push_back("clear all filters");
}

bool FilterFactory::isTypeOfFilter(FilterType type, const shared_ptr<ILogFilter>& filter) {
	switch (type) {
	case FilterType::ThreadId:
		return dynamic_pointer_cast<ThreadIdFilter>(filter) != nullptr;
	case FilterType::Cluster:
		return dynamic_pointer_cast<ClusterIdFilter>(filter) != nullptr;
	case FilterType::Io:
		return dynamic_pointer_cast<IOFilter>(filter) != nullptr;
	case FilterType::Quad:
		return dynamic_pointer_cast<QuadFilter>(filter) != nullptr;
	case FilterType::Unit:
		return dynamic_pointer_cast<UnitFilter>(filter) != nullptr;
	case FilterType::Area:
		return dynamic_pointer_cast<AreaFilter>(filter) != nullptr;
	}
	return false;
}

IViewPtr FilterFactory::createFilter(FilterType type, Variant& value) {
	switch (type) {
	case FilterType::ThreadId:
		if (holds_alternative<vector<int>>(value)) {
			return make_shared<ThreadIdFilter>(chain, get<vector<int>>(value));
		}
		else if (holds_alternative<int>(value)) {
			return make_shared<ThreadIdFilter>(chain, get<int>(value));
		}
		break;
	case FilterType::Cluster:
		return make_shared<ClusterIdFilter>(chain, get<Cluster>(value));
	case FilterType::Io:
		return make_shared<IOFilter>(chain, get<string>(value));
	case FilterType::Quad:
	{
		vector<int> vec = get<vector<int>>(value);
		if (vec.size() == 3) {
			return make_shared<QuadFilter>(chain, make_tuple(vec[0], vec[1], vec[2]));
		}
		throw invalid_argument("Vector size for Quad must be 3.");
	}
	case FilterType::Unit:
		return make_shared<UnitFilter>(chain, get<string>(value));
	case FilterType::Area:
		return make_shared<AreaFilter>(chain, get<string>(value));
	}
	return chain;
}

FilterFactory::~FilterFactory() {
	if (filterThread.joinable()) {
		filterThread.join();
	}
}

PYBIND11_MODULE(filter_factory_module, m) {
	m.doc() = "FilterFactory module: Provides functionality to apply filters to logs.";

	py::class_<Log>(m, "Log")
		.def(py::init<>())
		.def_readwrite("timeStamp", &Log::timeStamp)
		.def_readwrite("clusterId", &Log::clusterId)
		.def_readwrite("area", &Log::area)
		.def_readwrite("unit", &Log::unit)
		.def_readwrite("io", &Log::io)
		.def_readwrite("tid", &Log::tid)
		.def_readwrite("packet", &Log::packet);

	py::class_<Cluster>(m, "Cluster")
		.def(py::init<int, int, int, int, int>())
		.def(py::init<>())
		.def_readwrite("chip", &Cluster::chip)
		.def_readwrite("die", &Cluster::die)
		.def_readwrite("quad", &Cluster::quad)
		.def_readwrite("row", &Cluster::row)
		.def_readwrite("col", &Cluster::col)
		.def("__eq__", &Cluster::operator==)
		.def("__repr__", [](const Cluster& c) {
		return "<Cluster chip:" + std::to_string(c.chip) + ", die:" + std::to_string(c.die) +
			", quad:" + std::to_string(c.quad) + ", row:" + std::to_string(c.row) +
			", col:" + std::to_string(c.col) + ">";
			})
		.def("__hash__", [](const Cluster& c) {
		std::hash<Cluster> hasher;
		return hasher(c);
			});


	py::enum_<FilterType>(m, "FilterType")
		.value("Time", FilterType::Time, "Filter based on a specific timestamp.")
		.value("ThreadId", FilterType::ThreadId, "Filter based on thread identifier.")
		.value("Cluster", FilterType::Cluster, "Filter based on cluster identifier.")
		.value("TimeRange", FilterType::TimeRange, "Filter based on a range of timestamps.")
		.value("Io", FilterType::Io, "Filter based on IO type.")
		.value("Quad", FilterType::Quad, "Filter based on quadrant identifier.")
		.value("Unit", FilterType::Unit, "Filter based on unit identifier.")
		.value("Area", FilterType::Area, "Filter based on area identifier.");

	py::class_<FilterFactory>(m, "FilterFactory")
		.def(py::init<std::string>(), py::arg("logsFileName"), "Initialize FilterFactory with the given log file name.")
		.def("add_filter_to_chain", [](FilterFactory& self, std::pair<FilterType, Variant> filter) {
		self.addFilterToChain(filter);
			}, py::arg("filter"), "Add a new filter to the chain. The filter is a pair of FilterType and Variant.")
		.def("add_filter_to_chain", [](FilterFactory& self, std::pair<std::string, Variant> filter) {
		FilterType filterType = self.stringToFilterType(filter.first);
		self.addFilterToChain(std::make_pair(filterType, filter.second));
			}, py::arg("filter"), "Add a new filter to the chain. The filter is a pair of string (converted to FilterType) and Variant.")
		.def("set_end_time", py::overload_cast<time_t>(&FilterFactory::setEndTime), py::arg("time"), "Set the end time for filtering logs.")
		.def("set_start_time", py::overload_cast<time_t>(&FilterFactory::setStartTime), py::arg("time"), "Set the start time for filtering logs.")
		.def("remove_filter", &FilterFactory::removeFilter, py::arg("filterToRemove"), "Remove a specific filter from the chain. The filter to remove is specified as a pair of FilterType and Variant.")
		.def("remove_filter", [](FilterFactory& self, const std::string& filterToRemove) {
		FilterType filterType = self.stringToFilterType(filterToRemove);
		self.removeFilter(filterType);
			}, py::arg("filterToRemove"), "Remove a specific filter from the chain using a string.")
		.def("remove_last_filter", &FilterFactory::removeLastFilter, "Remove the last filter added to the chain.")
		.def("clear_filters", &FilterFactory::clearFilters, "Clear all filters and reset the filter chain to the initial state.")
		.def("start_logs", &FilterFactory::startLogs, "Apply filters and generate the filtered logs asynchronously.")
		.def("get_log", &FilterFactory::getLog, "Get the next filtered log.")
		.def("has_log", &FilterFactory::hasLog, "Check if there are more filtered logs.")
		.def("is_finished_process", &FilterFactory::isFinishProcess, "Check if the process has finished")
		.def("join_thread", &FilterFactory::joinThread, "Join the logs thread after filtering has completed.");
}