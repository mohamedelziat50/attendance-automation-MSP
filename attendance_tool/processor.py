import os, csv, re, validators


# File Name: Small Title, Class Name: Capitalized
class Processor:
    # Constructor With a single property: file path
    def __init__(self, file_path):
        self.file_path = file_path

    # Getter
    @property
    def file_path(self):
        return self._file_path

    # Setter
    @file_path.setter
    def file_path(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")
        self._file_path = file_path

    # Allow the proccesor to be printed immediatly if needed
    def __str__(self):
        """
        Handles medium files (500-5,000 rows) perfectly fine for our use case
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

    def validate(self):
        """
        Validates an entire CSV file's rows
        """
        try:
            with open(self.file_path) as file:
                reader = csv.DictReader(file)
                
                # Validate CSV structure first - To Avoid KeyError
                print("Field Names:", reader.fieldnames)
                self.validate_csv_headers(reader.fieldnames)

                valid_rows = []
                invalid_rows = []
                for row in reader:
                    try:
                        self.validate_name(row["Full Name"])
                        self.validate_email(row["University Email"])
                        self.validate_university_id(row["University ID"])
                        self.validate_course_code(row["Course Code"])
                        self.validate_course_time(row["Course Time"])
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

    def validate_csv_headers(self, fieldnames):
        """
        Validates CSV headers/columns exist.
            
        Raises ValueError: If any required column is missing or if headers are empty
        """
        if not fieldnames:
            raise ValueError("CSV file has no headers/columns")
        
        # All required columns that must be present
        required_columns = [
            "Full Name",
            "University Email", 
            "University ID",
            "Course Code",
            "Course Time"
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

    def validate_name(self, name):
        """
        Validates a person's name.
        Raises ValueError if invalid, returns nothing if valid.
        Regular Expressions Used
        """
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string")

        # Remove extra whitespace
        name = name.strip()

        if len(name) < 2:
            raise ValueError("Name must be at least 2 characters long")

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

        # No return needed - function succeeds if no exception is raised

    def validate_email(self, email):
        """
        Validates an email address.
        Raises ValueError if invalid, returns nothing if valid.
        Regular Expressions Not Used
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

    def validate_university_id(self, student_id):
        """
        Validates MIU student ID.
        Example: 2023/00824
        Format: YYYY/XXXXX (4-digit year / 5-digit number)
        Raises ValueError if invalid.
        Regular Expressions Not Used
        """
        if not student_id or not isinstance(student_id, str):
            raise ValueError("Student ID must be a non-empty string")

        # Remove extra whitespace
        student_id = student_id.strip()

        # Check if it contains exactly one forward slash
        if student_id.count("/") != 1:
            raise ValueError("Student ID must contain exactly one '/' separator")

        # Split by forward slash
        year_part, number_part = student_id.split("/")

        # Validate year part (4 digits)
        if not year_part.isdigit() or len(year_part) != 4:
            raise ValueError("Year part must be exactly 4 digits")

        # Check if year is reasonable (assuming students from 2010-2050)
        year = int(year_part)
        if year < 2010 or year > 2050:
            raise ValueError(f"Year must be between 2010-2050, got: {year}")

        # Validate number part (5 digits)
        if not number_part.isdigit() or len(number_part) != 5:
            raise ValueError("Student number must be exactly 5 digits")

        # No return needed - function succeeds if no exception is raised

    def validate_course_code(self, course_code):
        """
        Validates MIU course code.
        Format: At least 3 letters + at least 3 numbers + optional additional characters
        Examples: SWE11004, CSC101, MRK10105-BUS, ETH10104-CSC, BAS13104 Lecture, BAS13104 Tutorial
        Raises ValueError if invalid.
        Regular Expressions Used
        """
        if not course_code or not isinstance(course_code, str):
            raise ValueError("Course code must be a non-empty string")

        # Remove extra whitespace and convert to uppercase for consistency
        course_code = course_code.strip().upper()

        # Check minimum length (3 letters + 3 numbers = 6 characters minimum)
        if len(course_code) < 6:
            raise ValueError("Course code must be at least 6 characters long")

        # Check maximum reasonable length
        if len(course_code) >= 25:
            raise ValueError("Course code must be less than 26 characters")

        # Atleast 3 letters, then at least 3 digits, then optional letters/numbers/spaces/hyphens
        if not re.match(r"^[A-Z]{3,}[0-9]{3,}[A-Z0-9\s\-]*$", course_code):
            raise ValueError(
                "Course code must start with at least 3 letters, "
                "followed by at least 3 numbers, "
                "and optionally more letters/numbers/spaces/hyphens"
            )

        # No return needed - function succeeds if no exception is raised

    def validate_course_time(self, course_time):
        """
        Validates Course Time.
        Format: H:MM - H:MM, or H - H:MM, or H to H:MM (minutes optional & - or to seperator)
        Examples: 1:00 - 2:30, 11:30 - 1, 1 to 2:30, 9 - 10:15
        Raises ValueError if invalid.
        Regular Expressions Used
        """
        if not course_time or not isinstance(course_time, str):
            raise ValueError("Course time must be a non-empty string")

        course_time = course_time.strip()
        
        # Check for reasonable length
        if len(course_time) > 25:
            raise ValueError("Course time is too long")

        # Pattern to match: hour(optional :minutes) separator hour(optional :minutes)
        # Supports both " - " and " to " as separators
        """ 
        Regular Expression Explaination
        ([1-9]|1[0-2]) - Matches hours 1-12 (12-hour format), Utilizing OR
        (:[0-5][0-9])? - Optionally (with ?) matches :00 through :59
        \s+ - Matches one or more spaces
        (-|to) -  Matches either "-" or "to"
        """
        match = re.match(
            r"^([1-9]|1[0-2])(:[0-5][0-9])?\s+(-|to)\s+([1-9]|1[0-2])(:[0-5][0-9])?$",
            course_time,
        )
        if not match:
            raise ValueError(
                "Course time has an invalid format"
            )

        # Extract parts
        start_hour = int(match.group(1))
        start_minutes = match.group(2)  # Could be None or ":MM"
        separator = match.group(3)  # "-" or "to", No need to be validated since regex handles it
        end_hour = int(match.group(4))
        end_minutes = match.group(5)  # Could be None or ":MM"

        # Validate hours (1-12 for 12-hour format)
        self.validate_hour(start_hour)
        self.validate_hour(end_hour)

        # Validate minutes if present
        if start_minutes:
            minutes_value = int(start_minutes[1:])  # Remove the ":" using 'slicing'
            self.validate_minutes(minutes_value)

        if end_minutes:
            minutes_value = int(end_minutes[1:])  # Remove the ":" using 'slicing'
            self.validate_minutes(minutes_value)

    def validate_hour(self, hour):
        """
        Validates hours between 1-12.

        Raises ValueError: If hour is not between 1-12
        """
        if not (1 <= hour <= 12):
            raise ValueError(f"Hour must be between 1-12, got: {hour}")

    def validate_minutes(self, minutes):
        """
        Validates minutes between 0-59.
            
        Raises ValueError: If minutes is not between 0-59
        """
        if not (0 <= minutes <= 59):
            raise ValueError(f"Minutes must be between 0-59, got: {minutes}")
