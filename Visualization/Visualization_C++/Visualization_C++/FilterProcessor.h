#ifndef FILTERPROCESSOR_H
#define FILTERPROCESSOR_H

#include <string>
#include <vector>
#include "FilterFactory.h"

class FilterProcessor {
public:
    FilterProcessor(const std::string& inputFile, const std::vector<std::string>& filters, const std::string& outputFile);
    void processFilters();
    static void showFilterHelp();

private:
    std::string inputFile;
    std::vector<std::string> filters;
    std::string outputFile;
    void applyFilters(FilterFactory& filterFactory);
    static FilterType getFilterType(const string& type);
};

#endif
