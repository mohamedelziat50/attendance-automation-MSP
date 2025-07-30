# 3rd Party Packages
import argparse

# Our own package related, Syntax: from package.module import class/function
from attendance_tool.processor import Processor


def main():
    # 3rd Party Library to handle different cmd arguments
    parser = argparse.ArgumentParser()

    # Usage: output incase invalid command used
    parser.usage = "python main.py file.csv [--word | --pdf]"

    # Add Positional argument (do not start with - or --): required by default; no need for required=True
    parser.add_argument("csv_file", help="Path to the CSV file to process")

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

        # Handle Arguments
        if args.word:
            print("Exporting to Word document...")
            # TODO: Implement Word export functionality
            ...
        elif args.pdf:
            print("Exporting to PDF document...")
            # TODO: Implement PDF export functionality
            ...
        else:
            print("Launching GUI...")
            # TODO: Implement GUI functionality
            ...

    except FileNotFoundError as error:
        print(f"Error: {error}")
    except ValueError as error:
        print(f"Validation Error: {error}")
    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()
