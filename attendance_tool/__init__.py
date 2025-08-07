"""
Attendance Tool Package

A comprehensive attendance automation system for processing CSV attendance data,
validating student information, and generating formatted reports.

Modules:
- processor: CSV data validation and processing
- exporter: Word and PDF report generation
- argument_parser: Command-line interface handling

"""

# Import the main classes and functions to expose them for easy access
# This allows users to import everything they need from the package directly
# Instead of importing from submodules: from attendance_tool.processor import Processor
# They can now do: from attendance_tool import Processor

from .processor import Processor
from .exporter import Exporter
from .argument_parser import initialize_parser, validate_arguments
from .gui import launch_gui

__all__ = [
    "Processor",
    "Exporter",
    "initialize_parser",
    "validate_arguments",
    "launch_gui",
]
