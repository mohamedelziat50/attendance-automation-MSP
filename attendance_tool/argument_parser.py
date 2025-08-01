import argparse


def initialize_parser():
    """
    Configure a customized command line argument parser for attendance processing.
    
    Sets up argument parsing for CSV file processing with Word/PDF export options.
    Supports both GUI mode (no arguments) and command-line export mode.
    
    Returns:
        argparse.ArgumentParser: Configured parser with CSV file, export format, and title arguments
    """

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
        action="store_true",  # No value required after the flag (True Or False whether provided)
        help="Exports .csv file to .docx document immediately",
    )

    # --pdf argument
    group.add_argument(
        "--pdf",
        action="store_true",  # No value required after the flag (True Or False whether provided)
        help="Exports .csv file to .pdf document immediately",
    )

    # --title argument for Word/PDF documents
    parser.add_argument(
        "--title",  # Value required after the flag
        type=str,
        help="Title for the Word/PDF document (e.g., 'Monday 5/5/2025')",
    )

    return parser


def validate_arguments(parser, args):
    """
    Validate parsed command line arguments and determine application mode.
    
    Analyzes the provided arguments to determine whether to run in GUI mode
    or export mode, and validates that required arguments are present for each mode.
    
    Args:
        parser (argparse.ArgumentParser): The argument parser object for error reporting
        args (argparse.Namespace): Parsed command line arguments
        
    Returns:
        str: Application mode - either "gui" or "export"
        
    Raises:
        SystemExit: Via parser.error() if invalid argument combinations are provided
    """

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

    # If validation passes, return export mode
    return "export"
