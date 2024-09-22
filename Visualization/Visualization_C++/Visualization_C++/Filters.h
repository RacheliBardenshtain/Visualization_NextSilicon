#pragma once
#include "ILogFilter.h"
#include "PerformanceLogger.h"
#include <ctime>

class ThreadIdFilter : public ILogFilter {
private:
	vector<int> threadIds;

	void addThreadIds(const std::vector<int>& vec) {
		threadIds.insert(threadIds.end(), vec.begin(), vec.end());
	}

	void addThreadId(int tid) {
		threadIds.push_back(tid);
	}

public:
	template<typename T>
	ThreadIdFilter(IViewPtr toFilter, T arg)
		: ILogFilter(toFilter)
	{
		if constexpr (is_same_v<T, vector<int>>) {
			addThreadIds(arg);
		}
		else if constexpr (is_same_v<T, int>) {
			addThreadId(arg);
		}

		if (threadIds.size() == 1) {
			filterFunctions.push_back("ThreadIdFilter: " + to_string(threadIds[0]));
		}
		else {
			std::ostringstream oss;
			oss << "ThreadIdFilter: multiple THREADIDs - ";
			for (size_t i = 0; i < threadIds.size(); ++i) {
				oss << threadIds[i];
				if (i < threadIds.size() - 1) {
					oss << ", ";
				}
			}
			filterFunctions.push_back(oss.str());
		}
	}

	bool isToTake(const Log& l) const override {
		return find(threadIds.begin(), threadIds.end(), l.tid) != threadIds.end();
	}
};

class IOFilter : public ILogFilter {
private:
	string io;

public:
	IOFilter(IViewPtr toFilter, const string& i) : ILogFilter(toFilter), io(i)
	{
		filterFunctions.push_back("IOFilter: " + i);
	}

	bool isToTake(const Log& l) const override {
		return l.io == io;
	}
};

class QuadFilter : public ILogFilter {
private:
	tuple<int, int, int> quad;

public:
	QuadFilter(IViewPtr toFilter, tuple<int, int, int> q) : ILogFilter(toFilter), quad(q)
	{
		filterFunctions.push_back("QuadFilter: " + to_string(get<2>(quad)) + " in die: " + to_string(get<1>(quad)) + " in chip: " + to_string(get<1>(quad)));
	}

	bool isToTake(const Log& l) const override {
		return l.clusterId.chip == get<0>(quad) && l.clusterId.die == get<1>(quad) && l.clusterId.quad == get<2>(quad);
	}
};

class UnitFilter : public ILogFilter {
private:
	string unit;

public:
	UnitFilter(IViewPtr toFilter, const string& u) : ILogFilter(toFilter), unit(u)
	{
		filterFunctions.push_back("UnitFilter: " + u);
	}

	bool isToTake(const Log& l) const override {
		return l.unit == unit;
	}
};

class ClusterIdFilter : public ILogFilter {
private:
	Cluster clusterId;

public:
	ClusterIdFilter(IViewPtr toFilter, const Cluster& cid) : ILogFilter(toFilter), clusterId(cid)
	{
		stringstream ss;
		ss << cid;
		filterFunctions.push_back("ClusterIdFilter: " + ss.str());
	}

	bool isToTake(const Log& l) const override {
		return l.clusterId == clusterId;
	}
};

class AreaFilter : public ILogFilter {
private:
	string area;

public:
	AreaFilter(IViewPtr toFilter, const string& a) : ILogFilter(toFilter), area(a)
	{
		filterFunctions.push_back("AreaFilter: " + a);
	}

	bool isToTake(const Log& l) const override {
		return l.area == area;
	}
};
