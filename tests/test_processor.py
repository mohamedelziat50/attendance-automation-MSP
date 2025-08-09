from attendance_tool_msp.src.attendance_tool_msp import Processor
from pytest import raises

# Existing file with mixed valid and invalid data
valid_csv_file = "datasets/mixed_data.csv"


def test_init():
    # Test with non-existent file
    invalid_path = "datasets/not_exist.csv"
    with raises(FileNotFoundError):
        Processor(invalid_path)

    # Test with existing file that's not CSV
    invalid_csv_file = "datasets/USAGE.md"
    with raises(ValueError):
        Processor(invalid_csv_file)

    # Test with existing and valid file
    processor = Processor(valid_csv_file)
    assert processor is not None
    assert isinstance(processor, Processor)
    assert processor.file_path == valid_csv_file


def test_validate_csv_headers():
    """Test CSV header validation static method."""

    # Valid headers - NOTE: University Email is NOT required according to the function
    valid_headers = [
        "Full Name",
        "University ID",
        "Course Code",
        "Course Time",
        "Doctor/TA Name",
    ]
    Processor.validate_csv_headers(valid_headers)  # Should not raise

    # Extra headers including University Email - should not raise
    extra_headers = [
        "Full Name",
        "University Email",
        "University ID",
        "Course Code",
        "Course Time",
        "Doctor/TA Name",
        "Extra",
    ]
    Processor.validate_csv_headers(extra_headers)  # Should not raise

    # Headers from actual CSV file - should not raise
    actual_headers = [
        "Timestamp",
        "Full Name",
        "University Email",
        "University ID",
        "Course Code",
        "Course Time",
        "Doctor/TA Name",
    ]
    Processor.validate_csv_headers(actual_headers)  # Should not raise

    # Missing required headers
    missing_headers = [
        "Full Name",
        "University ID",
        "Course Code",
    ]  # Missing Course Time and Doctor/TA Name
    with raises(ValueError):
        Processor.validate_csv_headers(missing_headers)

    # Empty headers
    with raises(ValueError):
        Processor.validate_csv_headers([])


def test_validate_name():
    """Test name validation static method."""

    # Valid names - should return normalized names
    assert Processor.validate_name("john doe") == "John Doe"
    assert Processor.validate_name("ahmed al-hassan") == "Ahmed Al-Hassan"
    assert Processor.validate_name("MARY-JANE WATSON") == "Mary-Jane Watson"
    assert Processor.validate_name("o'connor") == "O'Connor"
    assert Processor.validate_name("sarah") == "Sarah"  # Single name is valid

    # Invalid names - should raise ValueError
    with raises(ValueError):
        Processor.validate_name("")

    with raises(ValueError):
        Processor.validate_name("   ")

    with raises(ValueError):
        Processor.validate_name("Ab")  # Too short (less than 3 chars)

    with raises(ValueError):
        Processor.validate_name("John123")  # Contains numbers

    with raises(ValueError):
        Processor.validate_name("John@Doe")  # Invalid characters

    with raises(ValueError):
        Processor.validate_name("A B C D E F")  # Too many words (>5)


def test_validate_email():
    """Test email validation static method for MIU domain only."""

    # Valid MIU emails - function validates but returns None
    assert Processor.validate_email("student@miuegypt.edu.eg") is None
    assert Processor.validate_email("john.doe@miuegypt.edu.eg") is None
    assert Processor.validate_email("STUDENT@MIUEGYPT.EDU.EG") is None

    # Invalid emails - not MIU domain
    with raises(ValueError):
        Processor.validate_email("student@gmail.com")

    with raises(ValueError):
        Processor.validate_email("user@university.edu")

    with raises(ValueError):
        Processor.validate_email("test@miuegypt.com")  # Wrong domain

    with raises(ValueError):
        Processor.validate_email("test@miuegypt.edu")  # Incomplete domain

    # Invalid email formats
    with raises(ValueError):
        Processor.validate_email("")

    with raises(ValueError):
        Processor.validate_email("invalid-email")

    with raises(ValueError):
        Processor.validate_email("@miuegypt.edu.eg")

    with raises(ValueError):
        Processor.validate_email("john.doe@@miuegypt.edu.eg")


def test_validate_university_id():
    """Test university ID validation for MIU format YYYY/XXXXX."""
    # Valid IDs - should return normalized format
    assert Processor.validate_university_id("2021/00123") == "2021/00123"
    assert Processor.validate_university_id("2023/45678") == "2023/45678"

    # Auto-format 9-digit IDs
    assert Processor.validate_university_id("202100123") == "2021/00123"
    assert Processor.validate_university_id("202345678") == "2023/45678"

    # Invalid IDs - should raise ValueError
    with raises(ValueError):
        Processor.validate_university_id("")

    with raises(ValueError):
        Processor.validate_university_id("   ")

    with raises(ValueError):
        Processor.validate_university_id(
            "123"
        )  # Doesn't contain exactly one forward slash

    with raises(ValueError):
        Processor.validate_university_id("abcd/1234")  # Letters in year

    with raises(ValueError):
        Processor.validate_university_id("2021/123X")  # Letters in number

    with raises(ValueError):
        Processor.validate_university_id("2009/12345")  # Year too old (<2010)

    with raises(ValueError):
        Processor.validate_university_id(
            "2021/123"
        )  # Number part too short (needs 5 digits)

    with raises(ValueError):
        Processor.validate_university_id("2021/123456")  # Number part too long


def test_validate_course_code():
    """Test course code validation for MIU format."""

    # Valid course codes - should return normalized codes
    assert Processor.validate_course_code("swe11004") == "SWE11004"
    assert Processor.validate_course_code("csc101") == "CSC101"
    assert Processor.validate_course_code("MRK10105-BUS") == "MRK10105-Bus"
    assert Processor.validate_course_code("BAS13104 Lecture") == "BAS13104 Lecture"
    assert Processor.validate_course_code("ETH10104-CSC") == "ETH10104-Csc"

    # Invalid course codes - should raise ValueError
    with raises(ValueError):
        Processor.validate_course_code("")

    with raises(ValueError):
        Processor.validate_course_code("   ")

    with raises(ValueError):
        Processor.validate_course_code("AB12")  # Too short (less than 6 chars)

    with raises(ValueError):
        Processor.validate_course_code("123ABC")  # Starts with numbers

    with raises(ValueError):
        Processor.validate_course_code("AB123")  # Only 2 letters (needs 3+)

    with raises(ValueError):
        Processor.validate_course_code("ABC12")  # Only 2 numbers (needs 3+)


def test_validate_course_time():
    """Test course time validation - NO AM/PM, 12-hour format only."""

    # Valid time formats - should return normalized H:MM - H:MM format
    assert Processor.validate_course_time("1:00 - 2:30") == "1:00 - 2:30"
    assert Processor.validate_course_time("11:30 - 1") == "11:30 - 1:00"
    assert Processor.validate_course_time("1 to 2:30") == "1:00 - 2:30"
    assert Processor.validate_course_time("9 - 10:15") == "9:00 - 10:15"
    assert Processor.validate_course_time("12-1") == "12:00 - 1:00"
    assert Processor.validate_course_time("1-2") == "1:00 - 2:00"

    # Invalid time formats - should raise ValueError
    with raises(ValueError):
        Processor.validate_course_time("")

    with raises(ValueError):
        Processor.validate_course_time("10:00 AM")  # AM/PM not supported

    with raises(ValueError):
        Processor.validate_course_time("13:00 - 14:00")  # 24-hour format not supported

    with raises(ValueError):
        Processor.validate_course_time("0 - 1")  # Hour 0 invalid (1-12 only)

    with raises(ValueError):
        Processor.validate_course_time("1:70 - 2")  # Invalid minutes

    with raises(ValueError):
        Processor.validate_course_time("13 - 1")  # Hour 13 invalid

    with raises(ValueError):
        Processor.validate_course_time("1 at 2")  # Invalid separator


def test_validate_hour():
    """Test hour validation for 12-hour format (1-12)."""

    # Valid hours - function validates but returns None
    assert Processor.validate_hour(1) is None
    assert Processor.validate_hour(12) is None
    assert Processor.validate_hour(6) is None

    # Invalid hours - should raise ValueError
    with raises(ValueError):
        Processor.validate_hour(0)  # Must be 1-12

    with raises(ValueError):
        Processor.validate_hour(13)  # Must be 1-12

    with raises(ValueError):
        Processor.validate_hour(-1)


def test_validate_minutes():
    """Test minutes validation (0-59)."""

    # Valid minutes - function validates but returns None
    assert Processor.validate_minutes(0) is None
    assert Processor.validate_minutes(30) is None
    assert Processor.validate_minutes(59) is None

    # Invalid minutes - should raise ValueError
    with raises(ValueError):
        Processor.validate_minutes(-1)

    with raises(ValueError):
        Processor.validate_minutes(60)

    with raises(ValueError):
        Processor.validate_minutes(75)


def test_validate_dr_ta_name():
    """Test doctor/TA name validation with title normalization."""

    # Valid instructor names - should return normalized names with titles
    assert Processor.validate_dr_ta_name("dr. smith") == "Dr. Smith"
    assert Processor.validate_dr_ta_name("prof. johnson") == "Prof. Johnson"
    assert Processor.validate_dr_ta_name("ta ahmed") == "TA Ahmed"
    assert (
        Processor.validate_dr_ta_name("john smith") == "Dr. John Smith"
    )  # Auto-adds Dr.
    assert Processor.validate_dr_ta_name("doctor jane doe") == "Dr. Jane Doe"
    assert Processor.validate_dr_ta_name("professor wilson") == "Prof. Wilson"
    assert Processor.validate_dr_ta_name("DR. SARAH WILSON") == "Dr. Sarah Wilson"

    # Invalid instructor names - should raise ValueError
    with raises(ValueError):
        Processor.validate_dr_ta_name("")

    with raises(ValueError):
        Processor.validate_dr_ta_name("   ")

    with raises(ValueError):
        Processor.validate_dr_ta_name("Dr.")  # Just title, no name

    with raises(ValueError):
        Processor.validate_dr_ta_name("Prof.")  # Just title, no name

    with raises(ValueError):
        Processor.validate_dr_ta_name("TA")  # Just title, no name

    with raises(ValueError):
        Processor.validate_dr_ta_name("Ab")  # Too short


def test_processor_integration():
    """Test processor with mixed valid/invalid data processing."""

    processor = Processor(valid_csv_file)

    # Process the file
    valid_rows, invalid_rows = processor.process()

    # Basic assertions
    assert isinstance(valid_rows, list)
    assert isinstance(invalid_rows, list)

    # With mixed data, we should have both valid and invalid rows
    assert len(valid_rows) > 0, "Should have some valid rows in mixed data"
    assert len(invalid_rows) > 0, "Should have some invalid rows in mixed data"

    # All required fields, email & timestamp are optional
    required_fields = [
        "Full Name",
        "University ID",
        "Course Code",
        "Course Time",
        "Doctor/TA Name",
    ]

    # Valid rows should have all required fields
    if valid_rows:
        first_valid = valid_rows[0]
        for field in required_fields:
            assert field in first_valid, f"Missing required field: {field}"

    # Invalid rows should have error field and preserve original data
    if invalid_rows:
        first_invalid = invalid_rows[0]
        assert "error" in first_invalid, "Invalid rows should have 'error' field"
        assert isinstance(first_invalid["error"], str)
        assert len(first_invalid["error"]) > 0, "Error message should not be empty"
        for field in required_fields:
            assert (
                field in first_invalid
            ), f"Required field '{field}' should be preserved in invalid rows"
