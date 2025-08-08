# NOTE:
# For local development with a src/ folder, use:
#   from attendance_tool_msp.src.attendance_tool_msp import (...)
# For installed packages (via pip), use:
#   from attendance_tool_msp import (...)
# The top-level import is standard for users installing your package from PyPI/TestPyPI.

# Previously (Before UV Restructuring): from attendance_tool_msp import (...)
# Our Own Package: Exposed functions and classes through __init__.py
from attendance_tool_msp.src.attendance_tool_msp import (
    Processor,
    Exporter,
    initialize_parser,
    validate_arguments,
    launch_gui,
)


def main():
    # Intialize argument parser with custom argument settings
    parser = initialize_parser()

    # Parse / Read Arguments
    args = parser.parse_args()

    # Validate arguments and determine mode
    mode = validate_arguments(parser, args)

    # GUI Mode:
    if mode == "gui":
        print("Launching GUI...")
        launch_gui()
        return

    # Export Mode:
    try:
        # Create processor with the provided CSV file
        processor = Processor(args.csv_file)
        valid_rows, invalid_rows = processor.process()

        # Print the file being processed on console
        print(f"Processing file: {processor.file_path}")

        # Initialize the exporter with title from command line arguments
        exporter = Exporter(valid_rows, invalid_rows, args.title)

        # Handle Arguments
        if args.word:
            print("Exporting to Word document...")
            filename = exporter.export_word()
            print("File Name:", filename)
        elif args.pdf:
            print("Exporting to PDF document...")
            filename = exporter.export_pdf()
            print("File Name:", filename)

    except FileNotFoundError as error:
        print(f"FileNotFoundError: {error}")
    except ValueError as error:
        print(f"ValueError: {error}")
    except PermissionError as error:
        print(f"Permission Error: {error}")
    except OSError as error:
        print(f"System Error: {error}")
    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()
