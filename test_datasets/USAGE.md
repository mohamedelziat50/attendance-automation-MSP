# Test Datasets for Attendance Automation System

This folder contains realistic test datasets for validating the attendance automation system. All data is fictional but mimics authentic student submission patterns and common errors.

## Dataset Files:

### 1. `valid_data.csv` (10 rows)
- **Purpose**: All data is valid and should pass validation
- **Expected Result**: All rows go to valid_rows, no errors
- **Use Case**: Testing successful processing flow

### 2. `invalid_data.csv` (10 rows)  
- **Purpose**: Contains realistic validation errors that actual students might make
- **Expected Result**: All rows go to invalid_rows with specific error messages
- **Use Case**: Testing error handling with authentic user mistakes
- **Common Errors**: Wrong email domains (@gmail.com), incomplete student IDs, short names, invalid course codes, incomplete instructor names

### 3. `mixed_data.csv` (15 rows)
- **Purpose**: Mix of valid data and realistic student errors (approximately 50/50)
- **Expected Result**: Some rows valid, some invalid with authentic error patterns
- **Use Case**: Testing real-world scenarios with mixed data quality
- **Realistic Issues**: Missing email parts, future graduation years, incomplete names, wrong domains

### 4. `no_email.csv` (8 rows)
- **Purpose**: Tests CSV files without email column
- **Expected Result**: All rows should be valid (email validation skipped)
- **Use Case**: Testing optional email validation feature

### 5. `time_formats.csv` (10 rows)
- **Purpose**: Tests various valid time formats
- **Expected Result**: All times normalized to H:MM - H:MM format
- **Use Case**: Testing time format normalization

### 6. `edge_cases.csv` (8 rows)
- **Purpose**: Tests boundary conditions and edge cases
- **Expected Result**: All should be valid (testing limits)
- **Use Case**: Testing validation boundary conditions

### 7. `small_data.csv` (3 rows)
- **Purpose**: Minimal dataset for quick testing
- **Expected Result**: All valid rows
- **Use Case**: Quick validation tests

### 8. `large_data.csv` (50 rows)
- **Purpose**: Large dataset to test system performance with more data
- **Expected Result**: All rows should be valid
- **Use Case**: Testing system with larger volumes of data

## Common Test Errors Included:

- **Names**: Too short (e.g., "Mo"), missing names
- **Emails**: Wrong domain (@gmail.com instead of @miuegypt.edu.eg), missing username parts
- **Student IDs**: Wrong format (missing zeros, wrong year like 2025), too short
- **Course Codes**: Missing letters (CS120 instead of CSC120), invalid formats
- **Times**: Invalid hours (25:00), wrong time ranges
- **Doctor Names**: Incomplete names ("Dr", "TA", "Prof")

## Usage:

```bash
# Test with valid data (all should pass)
python main.py test_datasets/valid_data.csv --word --title "Valid Test"

# Test with invalid data (all should fail)
python main.py test_datasets/invalid_data.csv --pdf --title "Invalid Test"

# Test with mixed data (some pass, some fail)
python main.py test_datasets/mixed_data.csv --word --title "Mixed Test"

# Test without email column (email validation skipped)
python main.py test_datasets/no_email.csv --pdf --title "No Email Test"

# Test time format normalization (all times should be H:MM - H:MM)
python main.py test_datasets/time_formats.csv --word --title "Time Format Test"

# Test edge cases and boundary conditions
python main.py test_datasets/edge_cases.csv --pdf --title "Edge Cases Test"

# Quick test with minimal data
python main.py test_datasets/small_data.csv --word --title "Small Data Test"

# Large dataset performance test
python main.py test_datasets/large_data.csv --pdf --title "Large Data Test"
```

All datasets follow the same structure as the main input.csv but with controlled data quality for specific testing scenarios.
