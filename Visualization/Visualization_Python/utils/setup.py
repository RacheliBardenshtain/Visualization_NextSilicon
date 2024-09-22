from setuptools import setup, Extension
import pybind11
import os

filter_cpp_files = [
    os.path.join('..', 'Visualization_C++', 'Visualization_C++', 'FilterFactory.cpp'),
    os.path.join('..', 'Visualization_C++', 'Visualization_C++', 'LogsFactory.cpp'),
    os.path.join('..', 'Visualization_C++', 'Visualization_C++', 'LogReader.cpp'),
    os.path.join('..', 'Visualization_C++', 'Visualization_C++', 'ILogFilter.cpp'),
    os.path.join('..', 'Visualization_C++', 'Visualization_C++', 'PerformanceLogger.cpp'),
]

ext_modules = [
    Extension(
        'logs_factory',
        [os.path.join('..', 'Visualization_C++', 'Visualization_C++', 'LogsFactory.cpp')],
        include_dirs=[pybind11.get_include()],
        extra_compile_args=['/std:c++17'],
    ),
    Extension(
        'filter_factory_module',
        filter_cpp_files,
        include_dirs=[pybind11.get_include()],
        extra_compile_args=['/std:c++20'],
    ),
]

setup(
    name="visualization_modules",
    ext_modules=ext_modules,
)