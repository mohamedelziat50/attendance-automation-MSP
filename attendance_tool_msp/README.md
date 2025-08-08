# attendance_tool_msp

A comprehensive Python package for automated attendance processing, validation, and professional report generation. Supports both command-line and GUI workflows for educators, organizations, and technical sessions.

## Features
- **CSV Attendance Processing:** Validate and process attendance sheets with robust error handling.
- **Data Validation:** Detects invalid records, missing fields, and edge cases.
- **Report Generation:** Export formatted attendance reports to Word and PDF.
- **Modern GUI:** Interactive, user-friendly interface built with CustomTkinter.
- **Command-Line Support:** Flexible CLI for batch processing and automation.
- **Extensible API:** Easily integrate into other Python projects.

## Installation
```bash
pip install attendance_tool_msp
```

## Usage

### API Example
```python
from attendance_tool_msp import Processor, Exporter, launch_gui

# Process attendance data
processor = Processor("data.csv")
valid_rows, invalid_rows = processor.process()

# Export to Word and PDF
exporter = Exporter(valid_rows, invalid_rows, title="Session Report")
exporter.export_word("report.docx")
exporter.export_pdf("report.pdf")

# Launch the GUI
launch_gui()
```

## Requirements
- Python 3.8+
- python-docx
- docx2pdf (optional, for PDF export)
- validators
- customtkinter
- pillow

## Documentation
- [Homepage](https://github.com/mohamedelziat50/attendance-automation-MSP)
- [Repository](https://github.com/mohamedelziat50/attendance-automation-MSP)

## License
MIT License
See the LICENSE file for details.
