#include "CLIHandler.h"
#include <iostream>
#include <fstream>

CLIHandler::CLIHandler(int argc, char** argv) : app("filter a huge log file", "filter") {
    setupCLIOptions();
    try {
        app.parse(argc, argv);
    }
    catch (const CLI::ParseError& e) {
        app.exit(e);
    }
}

void CLIHandler::setupCLIOptions() {
	app.add_option("-i,--input", inputFile, "Input log file")->required();
	app.add_option("-o,--output", outputFile, "Name of output filtered log file");
	app.add_option("-f,--filter", filters, "Filter criteria (format: type=value)");
	app.add_flag("-c,--processCounts", countFlag, "Count specific categories (TID, UNIT, AREA, CLUSTER, QUAD)");
	app.add_flag_callback("--help-filters", FilterProcessor::showFilterHelp, "Show help for filter formats");
}

void CLIHandler::execute() {
    if (app.get_option("--help")->count() || app.get_option("--help-filters")->count()) {
        return;
    }

    if (countFlag) {
        CountProcessor countProcessor(inputFile);
        countProcessor.processCounts();
        return;
    }

    FilterProcessor filterProcessor(inputFile, filters, outputFile);
    filterProcessor.processFilters();
}