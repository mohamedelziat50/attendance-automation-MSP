# 3rd Party Packages
import argparse

# Our own package related, Syntax: from package.module import class/function
from attendance_tool.processor import Processor
from attendance_tool.exporter import Exporter


def main():
    # 3rd Party Library to handle different cmd arguments
    parser = argparse.ArgumentParser()

    # Usage: output incase invalid command used
    parser.usage = 'python main.py [file.csv (--word | --pdf) --title "Title"]'

    # Add optional positional argument for CSV file, nargs=? means it's either provided
    #  or not provided, which allows for 2 different modes (GUI & cmd run)
    parser.add_argument("csv_file", nargs="?", help="Path to the CSV file to process")

    # Add title argument for Word/PDF documents
    parser.add_argument(
        "--title",
        type=str,
        help="Title for the Word/PDF document (e.g., 'Monday 5/5/2025')",
    )

    # Create a group to run either --word, --pdf, or no arguments at once
    group = parser.add_mutually_exclusive_group()

    # --word argument
    group.add_argument(
        "--word",
        action="store_true",
        help="Exports .csv file to .docx document immediately",
    )

    # --pdf argument
    group.add_argument(
        "--pdf",
        action="store_true",
        help="Exports .csv file to .pdf document immediately",
    )

    # Parse Arguments
    args = parser.parse_args()

    # Handle GUI mode (no arguments)
    if not args.csv_file:
        # If no CSV file but other arguments provided, it's an error
        if args.title or args.word or args.pdf:
            parser.error("CSV file is required when using --title, --word, or --pdf")
        print("Launching GUI...")
        # TODO: Implement GUI functionality
        return

    # Validate that all required arguments are provided for export mode
    if not args.word and not args.pdf:
        parser.error("Either --word or --pdf is required when providing a CSV file")
    if not args.title:
        parser.error("--title is required when providing a CSV file")

    # Get the CSV file path from arguments
    csv_file_path = args.csv_file

    try:
        # Create processor with the provided CSV file
        processor = Processor(csv_file_path)
        valid_rows, invalid_rows = processor.process()

        print(f"Processing file: {csv_file_path}")
        # print(f"Valid rows: {(valid_rows)}")
        # print(f"Invalid rows: {(invalid_rows)}")
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


if __name__ == "__main__":
    main()
