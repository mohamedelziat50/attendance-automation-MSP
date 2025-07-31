# 3rd Party Packages
import argparse

# Our own package related, Syntax: from package.module import class/function
from attendance_tool.processor import Processor
from attendance_tool.exporter import Exporter


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
            exporter.export_word()
        elif args.pdf:
            print("Exporting to PDF document...")
            # TODO: Implement PDF export functionality
            ...

    except FileNotFoundError as error:
        print(f"Error: {error}")
    except ValueError as error:
        print(f"Validation Error: {error}")
    except PermissionError as error:
        print(f"Error saving document: {error}")
    except Exception as error:
        print(f"Unexpected error: {error}")


def initialize_parser():
    """Configures a customised command line argument parser."""

    # 3rd Party Library to handle different cmd arguments
    parser = argparse.ArgumentParser(allow_abbrev=False)

    # Usage: output incase invalid command used
    parser.usage = 'python main.py [file.csv (--word | --pdf) --title "Title"]'

    # Add optional positional argument (no --) for CSV file, nargs=? means it's either provided
    # or not provided as the 1st argument, which allows for 2 different modes (GUI & CMD Modes)
    parser.add_argument("csv_file", nargs="?", help="Path to the CSV file to process")

    # Create a group to run either --word or --pdf one at time
    group = parser.add_mutually_exclusive_group()

    # --word argument
    group.add_argument(
        "--word",
        action="store_true", # No value required after the flag (True Or False whether provided)
        help="Exports .csv file to .docx document immediately",
    )

    # --pdf argument
    group.add_argument(
        "--pdf",
        action="store_true", # No value required after the flag (True Or False whether provided)
        help="Exports .csv file to .pdf document immediately",
    )

    # --title argument for Word/PDF documents
    parser.add_argument(
        "--title", # Value required after the flag
        type=str,
        help="Title for the Word/PDF document (e.g., 'Monday 5/5/2025')",
    )

    return parser


def validate_arguments(parser, args):
    """Validate the parsed command line arguments and return mode."""

    # Handle GUI mode (no arguments)
    if not args.csv_file:
        # If no CSV file but other arguments provided, it's an error
        if args.title or args.word or args.pdf:
            parser.error("CSV file is required when using --title, --word, or --pdf")
        # If no arguments are provided, then launch the GUI
        return "gui"

    # If we reached this point then csv_file is provided
    # Validate that --word or --pdf AND --title are provided for export mode
    if not args.word and not args.pdf:
        parser.error("Either --word or --pdf is required when providing a CSV file")
    if not args.title:
        parser.error("--title is required when providing a CSV file")

    # If no arguments are provided, then export mode
    return "export"


if __name__ == "__main__":
    main()
