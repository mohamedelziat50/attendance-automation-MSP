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

                valid_rows = []
                invalid_rows = []
                for row in reader:
                    try:
                        self.validate_name(row["Full Name"])
                        self.validate_email(row["University Email"])
                        self.validate_university_id(row["University ID"])
                        self.validate_course_code(row["Course Code"])
                        valid_rows.append(row)
                    except (ValueError, validators.ValidationError) as error:
                        # Capture the error message
                        row["error"] = str(error)  # Add error message to the row
                        invalid_rows.append(row)

                # Return a tuple of dictionaries
                return (valid_rows, invalid_rows)

        except FileNotFoundError:
            raise FileNotFoundError(f"Unable to open file: {self.file_path}")

    def validate_name(self, name):
        """
        Validates a person's name.
        Raises ValueError if invalid, returns nothing if valid.
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

        # Check for reasonable number of words (1-5 typically)
        words = name.split()
        if len(words) < 1 or len(words) > 5:
            raise ValueError("Name should contain 1-5 words")

        # No return needed - function succeeds if no exception is raised

    def validate_email(self, email):
        """
        Validates an email address.
        Raises ValueError if invalid, returns nothing if valid.
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
        """
        if not course_code or not isinstance(course_code, str):
            raise ValueError("Course code must be a non-empty string")
        
        # Remove extra whitespace and convert to uppercase for consistency
        course_code = course_code.strip().upper()
        
        # Check minimum length (3 letters + 3 numbers = 6 characters minimum)
        if len(course_code) < 6:
            raise ValueError("Course code must be at least 6 characters long")
        
        # Check maximum reasonable length
        if len(course_code) > 25:
            raise ValueError("Course code must be less than 25 characters")
        
        # Atleast 3 letters, then at least 3 digits, then optional alphanumeric/spaces/hyphens
        if not re.match(r"^[A-Z]{3,}[0-9]{3,}[A-Z0-9\s\-]*$", course_code):
            raise ValueError(
                "Course code must start with at least 3 letters, "
                "followed by at least 3 numbers, "
                "and optionally more letters/numbers/spaces/hyphens"
            )
        
        # No return needed - function succeeds if no exception is raised
