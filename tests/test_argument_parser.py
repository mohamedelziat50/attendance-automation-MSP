from attendance_tool_msp.src.attendance_tool_msp import initialize_parser, validate_arguments
from pytest import raises
import argparse


def test_initialize_parser():
    """Test parser initialization and configuration."""
    
    parser = initialize_parser()
    
    # Verify it's an ArgumentParser instance
    assert isinstance(parser, argparse.ArgumentParser)
    
    # Test usage string is set correctly
    expected_usage = 'python main.py [file.csv (--word | --pdf) --title "Title"]'
    assert parser.usage == expected_usage
    
    # Test that allow_abbrev (--wor or --p) is disabled (more strict parsing)
    assert parser.allow_abbrev == False


def test_gui_mode_validation():
    """Test validation logic for GUI mode (no arguments)."""
    
    parser = initialize_parser()
    
    # Valid GUI mode - no arguments at all
    args = parser.parse_args([])
    mode = validate_arguments(parser, args)
    assert mode == "gui"
    
    # Invalid GUI mode - CSV file missing but other args provided
    with raises(SystemExit):
        args = parser.parse_args(["--word"])
        validate_arguments(parser, args)
    
    with raises(SystemExit):
        args = parser.parse_args(["--pdf"])
        validate_arguments(parser, args)
        
    with raises(SystemExit):
        args = parser.parse_args(["--title", "Test Title"])
        validate_arguments(parser, args)

    with raises(SystemExit):
        args = parser.parse_args(["--word", "--title", "Test Title"])
        validate_arguments(parser, args)

    with raises(SystemExit):
        args = parser.parse_args(["--pdf", "--title", "Test Title"])
        validate_arguments(parser, args)


def test_export_mode_validation_valid():
    """Test validation logic for valid export mode combinations."""
    
    parser = initialize_parser()
    
    # Valid export mode - CSV + word + title
    args = parser.parse_args(["test.csv", "--word", "--title", "Test Report"])
    mode = validate_arguments(parser, args)
    assert mode == "export"
    assert args.csv_file == "test.csv"
    assert args.word == True
    assert args.pdf == False
    assert args.title == "Test Report"
    
    # Valid export mode - CSV + pdf + title
    args = parser.parse_args(["data.csv", "--pdf", "--title", "Test Report 2"])
    mode = validate_arguments(parser, args)
    assert mode == "export"
    assert args.csv_file == "data.csv"
    assert args.word == False
    assert args.pdf == True
    assert args.title == "Test Report 2"


def test_export_mode_validation_invalid():
    """Test validation logic for invalid export mode combinations."""
    
    parser = initialize_parser()
    
    # Invalid: CSV file provided but no export format
    with raises(SystemExit):
        args = parser.parse_args(["test.csv", "--title", "Test"])
        validate_arguments(parser, args)
    
    # Invalid: CSV file and export format but no title
    with raises(SystemExit):
        args = parser.parse_args(["test.csv", "--word"])
        validate_arguments(parser, args)
        
    with raises(SystemExit):
        args = parser.parse_args(["test.csv", "--pdf"])
        validate_arguments(parser, args)


def test_mutually_exclusive_export_formats():
    """Test that --word and --pdf are mutually exclusive."""
    
    parser = initialize_parser()
    
    # Should raise SystemExit when both --word and --pdf are provided
    with raises(SystemExit):
        parser.parse_args(["test.csv", "--word", "--pdf", "--title", "Test"])


def test_argument_parsing_details():
    """Test specific argument parsing behavior and types."""
    
    parser = initialize_parser()
    
    # Test CSV file as positional argument
    args = parser.parse_args(["myfile.csv", "--word", "--title", "Report"])
    assert args.csv_file == "myfile.csv"
    
    # Test that csv_file is optional (nargs="?")
    args = parser.parse_args([])
    assert args.csv_file is None
    
    # Test title argument accepts strings with spaces
    args = parser.parse_args(["test.csv", "--word", "--title", "Long Report Title"])
    assert args.title == "Long Report Title"
    
    # Test boolean flags default to False
    args = parser.parse_args([])
    assert args.word == False
    assert args.pdf == False


def test_argument_combinations_edge_cases():
    """Test edge cases and boundary conditions for argument combinations."""
    
    parser = initialize_parser()
    
    # Test with file path containing spaces (should work with quotes)
    args = parser.parse_args(["/path/with spaces/file.csv", "--pdf", "--title", "Test"])
    assert args.csv_file == "/path/with spaces/file.csv"
    
    # Test with empty title (should still parse, validation happens later)
    args = parser.parse_args(["test.csv", "--word", "--title", ""])
    assert args.title == ""
    
    # Test with special characters in title
    args = parser.parse_args(["test.csv", "--pdf", "--title", "Report @#$% 2025!"])
    assert args.title == "Report @#$% 2025!"


def test_help_messages():
    """Test that help messages are properly configured."""
    
    parser = initialize_parser()
    
    # Get help text
    help_text = parser.format_help()
    
    # Verify key help messages are present
    assert "Path to the CSV file to process" in help_text
    assert "Process CSV data and export attendance report as Word" in help_text
    assert "Process CSV data and export attendance report as PDF" in help_text
    assert "Title for the Word/PDF document" in help_text
