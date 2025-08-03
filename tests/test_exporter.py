from attendance_tool.exporter import Exporter
from attendance_tool.processor import Processor
from pytest import raises
import os

# Get real data from processor
processor = Processor("datasets/mixed_data.csv")
valid_rows, invalid_rows = processor.process()


def test_init():
    """Test Exporter initialization with valid and invalid inputs."""
    
    # Valid initialization
    exporter = Exporter(valid_rows, invalid_rows)
    assert isinstance(exporter, Exporter)
    assert exporter.title == "Attendance Report"
    
    exporter = Exporter([], [], "Custom Title")
    assert exporter.title == "Custom Title"
    
    # Test initialization with invalid valid_rows (calls setter)
    with raises(ValueError):
        Exporter("not a list", [])
    
    with raises(ValueError):
        Exporter(["not", "dictionaries"], [])
    
    # Test initialization with invalid invalid_rows (calls setter) 
    with raises(ValueError):
        Exporter([], "not a list")
        
    with raises(ValueError):
        Exporter([], ["not", "dictionaries"])
    
    # Test initialization with invalid title (calls setter)
    with raises(ValueError):
        Exporter([], [], "")  # Empty title
        
    with raises(ValueError):
        Exporter([], [], 123)  # Non-string title
        
    with raises(ValueError):
        Exporter([], [], "   ")  # Whitespace-only title


def test_valid_rows_property():
    """Test valid_rows getter and setter validation."""

    exporter = Exporter([], [])
    
    # Valid assignments
    exporter.valid_rows = valid_rows
    assert len(exporter.valid_rows) > 0
    
    exporter.valid_rows = []  # Empty list allowed
    assert len(exporter.valid_rows) == 0
    
    # Invalid type assignments - should raise ValueError
    with raises(ValueError):
        exporter.valid_rows = "not a list"
    
    with raises(ValueError):
        exporter.valid_rows = None
        
    with raises(ValueError):
        exporter.valid_rows = 123
    
    # Non-dictionary elements - should raise ValueError  
    with raises(ValueError):
        exporter.valid_rows = ["not", "dictionaries"]
        
    with raises(ValueError):
        exporter.valid_rows = [123, 456]


def test_invalid_rows_property():
    """Test invalid_rows getter and setter validation."""

    exporter = Exporter([], [])
    
    # Valid assignments
    exporter.invalid_rows = invalid_rows
    assert len(exporter.invalid_rows) > 0
    
    exporter.invalid_rows = []  # Empty list allowed
    assert len(exporter.invalid_rows) == 0
    
    # Invalid type assignments - should raise ValueError
    with raises(ValueError):
        exporter.invalid_rows = "not a list"
        
    with raises(ValueError):
        exporter.invalid_rows = None
        
    with raises(ValueError):
        exporter.invalid_rows = 123
    
    # Non-dictionary elements - should raise ValueError
    with raises(ValueError):
        exporter.invalid_rows = ["not", "dictionaries"]
        
    with raises(ValueError):
        exporter.invalid_rows = [123, 456]


def test_title_property():
    """Test title getter and setter validation."""

    exporter = Exporter([], [])
    
    # Valid assignments
    exporter.title = "Meeting Report"
    assert exporter.title == "Meeting Report"
    
    exporter.title = "Workshop Attendance 2025"
    assert exporter.title == "Workshop Attendance 2025"
    
    # Invalid type assignments - should raise ValueError
    with raises(ValueError):
        exporter.title = 123
        
    with raises(ValueError):
        exporter.title = []
        
    with raises(ValueError):
        exporter.title = None
    
    # Empty or whitespace-only strings - should raise ValueError
    with raises(ValueError):
        exporter.title = ""
        
    with raises(ValueError):
        exporter.title = "   "  # Only whitespace
        
    with raises(ValueError):
        exporter.title = "\t\n  "  # Various whitespace


def test_export_word():
    """Test Word document export."""

    exporter = Exporter(valid_rows, invalid_rows, "Word Test")
    
    filename = exporter.export_word()
    assert os.path.exists(filename)
    assert filename.endswith(".docx")
    assert os.path.getsize(filename) > 0
    os.remove(filename)


def test_export_pdf():
    """
    Test PDF document export.
    
    Note: PDF conversion may display Windows COM error messages (0x800706be/0x800706ba)
    due to Microsoft Word interface issues, but the PDF is still created successfully
    and the test will pass.
    """
    
    exporter = Exporter(valid_rows, invalid_rows, "PDF Test")

    filename = exporter.export_pdf()
    assert filename.endswith(".pdf")
    assert os.path.exists(filename)
    assert os.path.getsize(filename) > 0
    os.remove(filename)
