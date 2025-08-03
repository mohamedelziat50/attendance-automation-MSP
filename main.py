# 3rd Party Packages
...

# Our own package related, Syntax: from package.module import class/function
from attendance_tool.processor import Processor
from attendance_tool.exporter import Exporter
from attendance_tool.argument_parser import initialize_parser, validate_arguments


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
        # TODO: Implement GUI functionality
        return

    # Export Mode:
    try:
        # Create processor with the provided CSV file
        processor = Processor(args.csv_file)
        valid_rows, invalid_rows = processor.process()

        print(f"Processing file: {processor.file_path}")
        print("=======VALID=========")
        for row in valid_rows:
            print(row, end="\n\n")
        print("=======INVALID=========")
        for row in invalid_rows:
            print(row, end="\n\n")

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
