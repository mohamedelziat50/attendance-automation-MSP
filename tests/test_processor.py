from attendance_tool.processor import Processor
from pytest import raises

# Existing and valid file
valid_csv_file = "datasets/valid_data.csv"

def test_processor_init():
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

    

