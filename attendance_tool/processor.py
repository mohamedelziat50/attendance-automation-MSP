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

    # Allow the proccesor to be printed immediatly
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

                invalid_rows = []
                for row in reader:
                    try:
                        self.validate_name(row["Full Name"])
                        self.validate_email(row["University Email"])
                    except (ValueError, validators.ValidationError) as error:
                        # Capture the error message
                        row["error"] = str(error)  # Add error message to the row
                        invalid_rows.append(row)

                print("=========Not successful=============")
                for row in invalid_rows:
                    print(row, end="\n\n")

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

        email = email.strip()

        if not validators.email(email):
            raise ValueError(f"Invalid email format: {email}")

        # Check if email is from the required domain
        required_domain = "@miuegypt.edu.eg"
        if not email.lower().endswith(required_domain):
            raise ValueError(
                f"Email must be from {required_domain} domain, got: {email}"
            )

        # No return needed - function succeeds if no exception is raised
