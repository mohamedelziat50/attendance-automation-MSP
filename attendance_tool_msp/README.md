# Attendance Tool - MSP

An easy-to-use Python package for automated attendance processing, validation, and professional report generation. Built mainly for Microsoft Student Partners Tech Club (MSP), but works for any technical session or event at Misr International University (MIU).

## Features
- **CSV Attendance Processing:** Validate and process attendance sheets with robust error handling.
- **Data Validation:** Detects invalid records, missing fields, and edge cases.
- **Report Generation:** Export formatted attendance reports to Word and PDF.
- **Modern GUI:** Interactive, user-friendly interface built with CustomTkinter.
- **Command-Line Support:** Flexible CLI for batch processing and automation.
- **Extensible API:** Easily integrate into other Python projects.

## Installation
```bash
pip install attendance-tool-msp
```

## Usage

### CSV Format Requirements

Your CSV file **must** contain the following columns (headers):

- `Full Name`
- `University ID`
- `Course Code`
- `Course Time`
- `Doctor/TA Name`

These columns are required for successful processing. If any are missing or empty, the tool will raise an error and the file will not be processed.

> **Note:** Columns like `timestamp` and `email` are **not required**. The tool does not expect or require a timestamp column. The `University Email` column is only validated if present, but is not mandatory.


### Core Workflow: Processor + Exporter
Use `Processor` and `Exporter` together to process attendance data and generate reports:
```python
from attendance_tool_msp import Processor, Exporter

processor = Processor("data.csv")
valid_rows, invalid_rows = processor.process()

exporter = Exporter(valid_rows, invalid_rows, title="Session Report")
filename_word = exporter.export_word()
filename_pdf = exporter.export_pdf()
```

### Simple GUI Launch
If you prefer not to handle arguments or workflow, just launch the GUI with a single line:
```python
from attendance_tool_msp import launch_gui

launch_gui()
```

### Command-Line Integration
For CLI usage, use the argument parser helpers:
```python
from attendance_tool_msp import initialize_parser, validate_arguments

parser = initialize_parser()
args = parser.parse_args()
mode = validate_arguments(parser, args)
# Use mode to determine workflow (see documentation for details)
```

## Requirements
- Python 3.10+
- python-docx
- docx2pdf (optional, for PDF export)
- validators
- customtkinter
- pillow

## Documentation & Repository
- [Documentation](https://github.com/mohamedelziat50/attendance-automation-MSP)
- [Repository](https://yourdomain.com/docs)

## MIT License
For the most up-to-date license and project details, visit the [GitHub LICENSE](https://github.com/mohamedelziat50/attendance-automation-MSP/blob/main/LICENSE).
