#pragma once
#include <vector>
#include <variant>
#include <tuple>
#include "Generator.h"
#include "Log.h"

using namespace std;

using Variant = variant<string, double, int, Cluster, pair<int, int>, vector<int>, tuple<int, int, int>>;

class IView {
public:
    virtual Generator<Log> getNext() = 0;

    virtual bool isOpen() = 0;

    virtual ~IView() {}
};

typedef shared_ptr<IView> IViewPtr;