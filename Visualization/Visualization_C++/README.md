
# Advanced Processor Debugging Tool using DPC++

## Overview
The **Advanced Processor Debugging Tool** is a high-performance solution for analyzing and debugging processor activities by providing a real-time, visual representation of key components and processes. Designed with Intel’s oneAPI DPC++/SYCL, this tool leverages the full power of multi-threading and heterogeneous computing across CPUs and GPUs to deliver fast, scalable performance.

Additionally, the project integrates advanced design patterns, such as the **Decorator** pattern, to allow for flexible and extensible functionality. We also optimized response times by incorporating modern C++ features like **coroutines** and **generators**, ensuring smooth, efficient data processing.

The tool offers powerful log filtering features through the use of **Pybind11**, which bridges the C++ backend with Python, allowing users to easily filter and analyze log data in the visual part of the project.

## Key Features
- **Real-time Visualization**: Track processor components and operations as they happen.
- **Cross-Platform Computing**: Leverages DPC++ for optimal performance on both CPUs and GPUs.
- **Advanced Filtering**: Supports various filtering options for logs, integrated with Python using Pybind11.
- **Design Patterns**: Implements the **Decorator** pattern for extendable log filtering functionalities.
- **Optimized Performance**: Uses **coroutines** and **generators** to improve runtime efficiency and responsiveness.

## Installation and Setup
To get started, ensure you have the following prerequisites installed:

- [Intel oneAPI](https://www.intel.com/content/www/us/en/developer/tools/oneapi/base-toolkit-download.html)
- [Pybind11](https://github.com/pybind11/pybind11)
- [spdlog](https://github.com/gabime/spdlog/tree/v1.14.1) (version 1.14.1)
- [Python 3.12](https://www.python.org/downloads/release/python-312/)

### Setup Instructions
1. Install Intel's oneAPI Base Toolkit on your machine.
2. Download and install the `spdlog` logging library.
3. Set up Python 3.12 with Pybind11 for C++/Python integration.
4. Compile and run the project using your preferred development environment.

## Usage Guide

### Log File Filtering
To filter an existing log file and generate a refined log, use the following command:
```bash
Visualization_C++.exe -i <full path to original log file> -o <filtered file name> -f <filter format>
```

### Available Filter Options
- **TimeRange**: Filters logs between specific start and end times (e.g., `TimeRange=1726671491.525302,1726671531.525302`).
- **Time**: Filters logs matching a specific timestamp (e.g., `Time=1726671491.525302`).
- **Quad**: Quad=Chip:<value>,Die:<value>,Quad:<value> (e.g., `Quad=Chip:0,Die:1,Quad:2`).
- **ThreadId**: Filters logs by thread IDs (e.g., `ThreadId=7,10,15`).
- **Unit**: Filters logs by processor units (e.g., `Unit=iqr`).
- **Area**: Filters logs by processor areas (e.g., `Area=bmt`).
- **Cluster**: Filters logs by cluster (chip, die, quad, row, column) (e.g., `Cluster=chip:0, die:1, quad:2, row:3, col:4`).

### Interactive Log Count Mode
To enter interactive mode and dynamically count parameters from the log file, run:
```bash
Visualization_C++.exe -i <full path to original log file> -c
```
This mode allows you to count occurrences of parameters like Thread IDs, Units, Areas, Clusters, and Quads in real-time. Once logs are processed, you will be prompted to select the count type:
```
What do you want to count? (TID, UNIT, AREA, CLUSTER, QUAD):
To exit - enter Exit
```
Select one of the options, or type `Exit` to leave the counting mode.

## Example Commands
- **Filtering by Time Range**:
  ```bash
  Visualization_C++.exe -i logs/log1.csv -o filtered_logs.csv -f "TimeRange=1726671491.525302,1726671531.525302"
  ```
- **Counting Thread IDs**:
  ```bash
  Visualization_C++.exe -i logs/log1.csv -c
  ```

## Contributors
This project was developed by a talented and dedicated team:
- [Rachel Bardenshtain](https://github.com/RacheliBardenshtain)
- [Chaya Avramovitz](https://github.com/chayaleA)
- [Elisheva Volpo](https://github.com/Elisheva-Volpo)
- [Nechama Sha](https://github.com/Nechama-Sha)

Feel free to contribute or provide suggestions to make this tool even more powerful.
