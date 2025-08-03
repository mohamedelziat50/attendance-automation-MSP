import os, csv, re, validators
from datetime import datetime


# File Name: Small Title, Class Name: Capitalized
class Processor:
    """
    CSV validation and processing class for attendance data.

    Attributes:
        file_path (str): Path to the CSV file to process
    """

    # Constructor With a single property: file path
    def __init__(self, file_path):
        """
        Initialize the Processor with CSV file path.

        Args:
            file_path (str): Path to the CSV file to process
        """
        self.file_path = file_path

    # Getter
    @property
    def file_path(self):
        """
        Get the CSV file path.

        Returns:
            str: The path to the CSV file
        """
        return self._file_path

    # Setter
    @file_path.setter
    def file_path(self, file_path):
        """
        Set CSV file path with validation.

        Args:
            file_path (str): Path to the CSV file to process

        Returns:
            None: This setter does not return a value

        Raises:
            FileNotFoundError: If file does not exist
            ValueError: If file is not a CSV file
        """
        # Check if file exists first
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")
        # Then check it's a csv file
        if not file_path.endswith(".csv"):
            raise ValueError(f"The file '{file_path}' is not a .csv file")
        self._file_path = file_path

    def __str__(self):
        """
        Returns string representation of CSV data for debugging.
        Handles small-medium sized CSV files (1-5000 rows).

        Returns:
            str: Formatted CSV data or appropriate message if file is empty

        Raises:
            FileNotFoundError: If CSV file cannot be opened
        """
        try:
            with open(self.file_path) as file:
                reader = csv.DictReader(file)

                rows = []
                for row in reader:
                    rows.append(str(row))

                if not rows:
                    return f"No data found in '{self.file_path}' file"

                # Join with newlines for readable output
                return "\n\n".join(rows)
        except FileNotFoundError:
            raise FileNotFoundError(f"Unable to open file: {self.file_path}")

    def process(self):
        """
        Validates CSV file and returns valid and invalid data.

        Returns:
            tuple: (valid_rows, invalid_rows) as lists of dictionaries

        Raises:
            FileNotFoundError: If CSV file cannot be opened
            ValueError: If CSV headers are invalid or missing
        """
        try:
            with open(self.file_path) as file:
                reader = csv.DictReader(file)

                # Strip whitespace from field names, to avoid headers like 'Full Name  '
                if reader.fieldnames:
                    reader.fieldnames = [field.strip() for field in reader.fieldnames]

                # Validate CSV structure first - To Avoid KeyError
                print("Field Names:", reader.fieldnames)
                Processor.validate_csv_headers(reader.fieldnames)

                valid_rows = []
                invalid_rows = []
                for row in reader:
                    try:
                        # Only validate email if the column exists in CSV headers
                        if "University Email" in reader.fieldnames:
                            Processor.validate_email(row["University Email"])

                        # Validate Required Columns
                        row["Full Name"] = Processor.validate_name(
                            row["Full Name"]
                        )  # Normalize student name
                        row["University ID"] = Processor.validate_university_id(
                            row["University ID"]
                        )  # Normalize and validate student ID
                        row["Course Code"] = Processor.validate_course_code(
                            row["Course Code"]
                        )  # Normalize course code to uppercase
                        row["Course Time"] = Processor.validate_course_time(
                            row["Course Time"]
                        )  # Normalize course time format
                        row["Doctor/TA Name"] = Processor.validate_dr_ta_name(
                            row["Doctor/TA Name"]
                        )  # Normalize instructor name

                        # Append valid row if all validations pass
                        valid_rows.append(row)
                    except (ValueError, validators.ValidationError) as error:
                        # Capture the error message
                        row["error"] = str(error)  # Add error message to the row
                        invalid_rows.append(row)

                # Return a tuple of dictionaries
                return (valid_rows, invalid_rows)

        except FileNotFoundError:
            raise FileNotFoundError(f"Unable to open file: {self.file_path}")
        except ValueError as error:
            raise ValueError(f"CSV validation failed: {error}")

    @staticmethod
    def validate_csv_headers(fieldnames):
        """
        Validates that all required CSV headers are present.

        Args:
            fieldnames (list): List of column headers from CSV file

        Returns:
            None: This function does not return a value, it only validates

        Raises:
            ValueError: If columns/headers are missing or empty
        """
        if not fieldnames:
            raise ValueError("CSV file has no headers/columns")

        # All required columns that must be present
        required_columns = [
            "Full Name",
            "University ID",
            "Course Code",
            "Course Time",
            "Doctor/TA Name",
        ]

        # Check each required column one by one
        for column in required_columns:
            if column not in fieldnames:
                raise ValueError(f"Missing required column: {column}")

        # Check for None or empty headers
        # enumerate(fieldnames) gives us both the index and the value
        for i, header in enumerate(fieldnames):
            if not header or header.strip() == "":
                raise ValueError(f"Empty column header found at position: {i}")

    @staticmethod
    def validate_name(name):
        """
        Validates and normalizes a person's full name.
        Automatically capitalizes each word for consistent formatting.
        Regular expressions are used.

        Args:
            name (str): The full name to validate

        Returns:
            str: Validated and properly capitalized name

        Raises:
            ValueError: If name is invalid
        """
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string")

        # Remove extra whitespace
        name = name.strip()

        if len(name) < 3:
            raise ValueError("Name must be at least 3 characters long")

        if len(name) > 50:
            raise ValueError("Name must be less than 50 characters")

        # Check for valid characters (letters, spaces, hyphens, apostrophes)
        if not re.match(r"^[a-zA-Z\s'-]+$", name):
            raise ValueError(
                "Name can only contain letters, spaces, hyphens, and apostrophes"
            )

        # Check for reasonable number of words (1-5 typically for a full name)
        words = name.split()
        if len(words) < 1 or len(words) > 5:
            raise ValueError("Name should contain 1-5 words")

        # Capitalize each word for consistent formatting
        name = name.title()

        return name

    @staticmethod
    def validate_email(email):
        """
        Validates university email addresses.
        Regular expressions are not used.

        Args:
            email (str): The email address to validate

        Returns:
            None: This function does not return a value, it only validates

        Raises:
            ValueError: If email is invalid or not from required domain
        """
        if not email or not isinstance(email, str):
            raise ValueError("Email must be a non-empty string")

        # Remove extra whitespace
        email = email.strip()

        # Check if it's an actual email using 3rd party library
        if not validators.email(email):
            raise ValueError(f"Invalid email format: {email}")

        # Check if email is from the required domain
        required_domain = "@miuegypt.edu.eg"
        if not email.lower().endswith(required_domain):
            raise ValueError(
                f"Email must be from {required_domain} domain, got: {email}"
            )

        # No return needed - function succeeds if no exception is raised

    @staticmethod
    def validate_university_id(student_id):
        """
        Validates MIU student ID format (YYYY/XXXXX).
        Auto-formats 9-digit IDs without slashes to YYYY/XXXXX format.
        Regular expressions are not used.

        Examples:
            2023/00824, 2020/34125, 202306246 (auto-formatted to 2023/06246)

        Args:
            student_id (str): The student ID to validate

        Returns:
            str: Validated and normalized student ID in YYYY/XXXXX format

        Raises:
            ValueError: If student ID format is invalid
        """
        if not student_id or not isinstance(student_id, str):
            raise ValueError("Student ID must be a non-empty string")

        # Remove extra whitespace
        student_id = student_id.strip()

        # Auto-format if no slash but exactly 9 digits (YYYYXXXXX format)
        if "/" not in student_id and student_id.isdigit() and len(student_id) == 9:
            student_id = student_id[:4] + "/" + student_id[4:]

        # Check if it contains exactly one forward slash
        if student_id.count("/") != 1:
            raise ValueError(
                "Student ID must contain exactly one '/' separator or be 9 digits (YYYYXXXXX)"
            )

        # Split by forward slash
        year_part, number_part = student_id.split("/")

        # Validate year part (4 digits)
        if not year_part.isdigit() or len(year_part) != 4:
            raise ValueError("Year part must be exactly 4 digits")

        # Check if year is reasonable (assuming students from atleast 2010 to current year)
        year = int(year_part)
        current_year = datetime.now().year  # Dynamic current year

        if year < 2010 or year > current_year:
            raise ValueError(f"Year must be between 2010-{current_year}, got: {year}")

        # Validate number part (5 digits)
        if not number_part.isdigit() or len(number_part) != 5:
            raise ValueError("Student number must be exactly 5 digits")

        # Return the normalized student ID with slash
        return student_id

    @staticmethod
    def validate_course_code(course_code):
        """
        Validates MIU course code format.
        At least 3 letters + at least 3 numbers + optional additional characters including parentheses.
        Normalizes format with proper capitalization.
        Regular expressions are used.

        Examples:
            SWE11004, CSC101, MRK10105-BUS, ETH10104-CSC, BAS13104 Lecture, BAS13104 Tutorial, BAS1120301 (Tutorial)

        Args:
            course_code (str): The course code to validate

        Returns:
            str: Validated and normalized course code with proper capitalization

        Raises:
            ValueError: If course code format is invalid
        """
        if not course_code or not isinstance(course_code, str):
            raise ValueError("Course code must be a non-empty string")

        # Remove extra whitespace
        course_code = course_code.strip()

        # Check minimum length (3 letters + 3 numbers = 6 characters minimum)
        if len(course_code) < 6:
            raise ValueError("Course code must be at least 6 characters long")

        # Check maximum reasonable length
        if len(course_code) >= 25:
            raise ValueError("Course code must be less than 26 characters")

        # Simple normalization: uppercase the first 3 letters, keep the rest as is
        if len(course_code) >= 3:
            course_code = course_code[:3].upper() + course_code[3:].title()

        # Atleast 3 letters, then at least 3 digits, then optional letters/numbers/spaces/hyphens/parentheses
        if not re.match(
            r"^[A-Z]{3,}[0-9]{3,}[A-Z0-9\s\-()]*$", course_code, re.IGNORECASE
        ):
            raise ValueError(
                "Course code must start with at least 3 letters, "
                "followed by at least 3 numbers, "
                "and optionally more letters/numbers/spaces/hyphens/parentheses"
            )

        # Return the normalized uppercase course code
        return course_code

    @staticmethod
    def validate_course_time(course_time):
        """
        Validates course time format and returns normalized H:MM - H:MM format.
        Supports formats like H:MM - H:MM, H - H:MM, H to H:MM (minutes optional, - or to separator).
        AM/PM indicators are NOT supported.
        Regular expressions are used.

        Examples:
            1:00 - 2:30, 11:30 - 1, 1 to 2:30, 9 - 10:15

        Args:
            course_time (str): The course time to validate

        Returns:
            str: Normalized course time in H:MM - H:MM format

        Raises:
            ValueError: If course time format is invalid
        """
        if not course_time or not isinstance(course_time, str):
            raise ValueError("Course time must be a non-empty string")

        course_time = course_time.strip()

        # Check for reasonable length
        if len(course_time) > 25:
            raise ValueError("Course time is too long")

        # Pattern to match: hour(optional :minutes) separator hour(optional :minutes)
        # Supports both " - " and " to " as separators with optional spaces
        """ 
        Regular Expression Explaination
        ([1-9]|1[0-2]) - Matches hours 1-12 (12-hour format), Utilizing OR
        (:[0-5][0-9])? - Optionally (with ?) matches :00 through :59
        \\s* - Matches zero or more spaces (optional whitespace)
        (-|to) -  Matches either "-" or "to"
        \\s* - Matches zero or more spaces (optional whitespace)
        """
        match = re.match(
            r"^([1-9]|1[0-2])(:[0-5][0-9])?\s*(-|to)\s*([1-9]|1[0-2])(:[0-5][0-9])?$",
            course_time,
        )
        if not match:
            raise ValueError("Course time has an invalid format")

        # Extract parts
        start_hour = int(match.group(1))
        start_minutes = match.group(2)  # Could be None or ":MM"
        separator = match.group(
            3
        )  # "-" or "to", No need to be validated since regex handles it
        end_hour = int(match.group(4))
        end_minutes = match.group(5)  # Could be None or ":MM"

        # Validate hours (1-12 for 12-hour format)
        Processor.validate_hour(start_hour)
        Processor.validate_hour(end_hour)

        # Validate minutes if present
        if start_minutes:
            minutes_value = int(start_minutes[1:])  # Remove the ":" using 'slicing'
            Processor.validate_minutes(minutes_value)

        if end_minutes:
            minutes_value = int(end_minutes[1:])  # Remove the ":" using 'slicing'
            Processor.validate_minutes(minutes_value)

        # Format and return normalized time as H:MM - H:MM
        start_time = f"{start_hour}{start_minutes if start_minutes else ':00'}"
        end_time = f"{end_hour}{end_minutes if end_minutes else ':00'}"
        return f"{start_time} - {end_time}"

    @staticmethod
    def validate_hour(hour):
        """
        Helper method for course time validation - validates hour values for 12-hour time format.

        Args:
            hour (int): Hour value to validate

        Returns:
            None: This function does not return a value, it only validates

        Raises:
            ValueError: If hour is not between 1-12 (inclusive)
        """
        if not (1 <= hour <= 12):
            raise ValueError(f"Hour must be between 1-12, got: {hour}")

    @staticmethod
    def validate_minutes(minutes):
        """
        Helper method for course time validation - validates minute values for time format.

        Args:
            minutes (int): Minute value to validate

        Returns:
            None: This function does not return a value, it only validates

        Raises:
            ValueError: If minutes is not between 0-59 (inclusive)
        """
        if not (0 <= minutes <= 59):
            raise ValueError(f"Minutes must be between 0-59, got: {minutes}")

    @staticmethod
    def validate_dr_ta_name(name):
        """
        Validates and normalizes instructor names (Doctor/TA).
        Similar functionality to validate_name but allows for titles like "Dr.", "TA", and "Prof.".
        Auto-adds "Dr." prefix if no title is detected anywhere in the name.
        Regular expressions are used.

        Args:
            name (str): The instructor's name to validate

        Returns:
            str: Normalized instructor name with appropriate title prefix

        Raises:
            ValueError: If name is invalid
        """
        if not name or not isinstance(name, str):
            raise ValueError("Doctor/TA name must be a non-empty string")

        # Remove extra whitespace
        name = name.strip()

        if len(name) < 3:
            raise ValueError("Doctor/TA name must be at least 3 characters long")

        if len(name) > 60:
            raise ValueError("Doctor/TA name must be less than 60 characters")

        # Check if it's just a title without a name (incomplete)
        incomplete_titles = [
            "dr",
            "prof",
            "ta",
            "professor",
            "doctor",
            "dr.",
            "prof.",
            "ta.",
        ]
        if name.lower().strip() in incomplete_titles:
            raise ValueError(
                "Doctor/TA name cannot be just a title, must include actual name"
            )

        # Check for valid characters (letters, spaces, hyphens, apostrophes, periods, parentheses for titles)
        if not re.match(r"^[a-zA-Z\s'.\-()]+$", name):
            raise ValueError(
                "Doctor/TA name can only contain letters, spaces, hyphens, apostrophes, periods, and parentheses"
            )

        # Check for reasonable number of words (1-6 to allow for titles like "Dr. John Smith")
        words = name.split()
        if len(words) < 1 or len(words) > 6:
            raise ValueError("Doctor/TA name should contain 1-6 words")

        # Normalize instructor title and auto-add "Dr." prefix if needed
        name = Processor.__normalize_instructor_title(name)

        # Return the potentially modified name
        return name

    @staticmethod
    def __normalize_instructor_title(name):
        """
        Helper method to detect, standardize, and normalize instructor titles.

        Automatically detects existing titles (Dr./Doctor, Prof./Professor, TA) and standardizes
        their format. If no title is detected, automatically adds "Dr." prefix.

        Uses word boundary regex patterns to avoid false matches (e.g., "ta" in "Tamer").

        Args:
            name (str): The instructor's name to normalize

        Returns:
            str: Normalized name with standardized title format:
                - "Dr." for doctor/dr variations
                - "Prof." for professor/prof variations
                - "TA" for ta variations (no period)
                - "Dr. {name}" for names without detected titles

        Examples:
            "john smith" -> "Dr. John Smith"
            "doctor jane doe" -> "Dr. Jane Doe"
            "prof smith" -> "Prof. Smith"
            "ta mike" -> "TA Mike"
            "tamer ibrahim" -> "Dr. Tamer Ibrahim" (avoids false "ta" match)
            "DR. SARAH wilson" -> "Dr. Sarah Wilson"
        """
        name_lower = name.lower()

        # First, capitalize the entire name to ensure proper case
        name = name.title()

        # Then check what type of title exists and standardize accordingly
        # Use word boundaries (\b) to avoid false matches (e.g., "ta" in "Tamer")

        if re.search(r"\b(doctor|dr)\b", name_lower):
            # Replace any doctor/dr variations with "Dr." - avoid double periods
            name = re.sub(r"\b(doctor|dr\.?)\b", "Dr.", name, flags=re.IGNORECASE)
            # Fix any double periods that might occur
            name = name.replace("Dr..", "Dr.")
        elif re.search(r"\b(professor|prof)\b", name_lower):
            # Replace any professor/prof variations with "Prof." - avoid double periods
            name = re.sub(
                r"\b(professor|prof\.?)\b", "Prof.", name, flags=re.IGNORECASE
            )
            # Fix any double periods that might occur
            name = name.replace("Prof..", "Prof.")
        elif re.search(r"\bta\b", name_lower):
            # Replace any TA variations with "TA" (no dot)
            name = re.sub(r"\bta\.?\b", "TA", name, flags=re.IGNORECASE)
        else:
            # No title found, add "Dr." prefix (name is already capitalized)
            name = f"Dr. {name}"

        return name
