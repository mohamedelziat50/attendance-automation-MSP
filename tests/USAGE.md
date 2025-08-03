# Tests Usage Guide

This folder contains comprehensive test suites for the attendance automation system components.

## Running Tests

### Run All Tests
```bash
python -m pytest tests/ -v
```

### Run Individual Test Files
```bash
# Test processor (CSV validation and processing)
python -m pytest tests/test_processor.py -v

# Test exporter (Word/PDF document generation)
python -m pytest tests/test_exporter.py -v

# Test argument parser (command-line interface)
python -m pytest tests/test_argument_parser.py -v
```

## Prerequisites
- Ensure `datasets/mixed_data.csv` file exists (required for processor tests)
- `pytest` framework installed
- Microsoft Word installed (for PDF conversion testing)

## Test Files Overview

### `test_processor.py` (11 tests)
- CSV file validation and data processing
- Static method validation (names, emails, IDs, etc.)
- Integration testing with real data from `datasets/mixed_data.csv`

### `test_exporter.py` (6 tests)
- Document export functionality (Word and PDF)
- Property validation and error handling
- **⚠️ PDF Test Note**: May display Windows COM error messages during PDF conversion (e.g., `0x800706be`). These are cosmetic errors - the PDF is still created successfully and the test will pass.

### `test_argument_parser.py` (8 tests)
- Command-line argument parsing and validation
- GUI vs Export mode logic testing
- Help message and usage validation

## Total Coverage
- **25 tests** covering all core functionality
- Real data integration for comprehensive validation
- Exception handling and edge case testing

## Command Note

Using `python -m pytest tests/file.py -v` instead of `pytest file.py` means:
- Use the current Python interpreter
- Run pytest as a module
- Test only the file.py file
- Show verbose output with detailed results **(Visually Better)**
