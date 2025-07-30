import docx

class Exporter:
    # Constructor with valid and invalid rows
    def __init__(self, valid_rows, invalid_rows):
        self.valid_rows = valid_rows
        self.invalid_rows = invalid_rows

    # Getter for valid_rows
    @property
    def valid_rows(self):
        return self._valid_rows

    # Setter for valid_rows: Empty Lists are allowed
    @valid_rows.setter
    def valid_rows(self, valid_rows):
        if not isinstance(valid_rows, list):
            raise ValueError("Valid rows must be a list")
        # Check if list is not empty and first item is dict
        if valid_rows and not isinstance(valid_rows[0], dict):
            raise ValueError("Valid rows data must be dictionaries")
        self._valid_rows = valid_rows

    # Getter for invalid_rows
    @property
    def invalid_rows(self):
        return self._invalid_rows

    # Setter for invalid_rows: Empty Lists are allowed
    @invalid_rows.setter
    def invalid_rows(self, invalid_rows):
        if not isinstance(invalid_rows, list):
            raise ValueError("Invalid rows must be a list")
        # Check if list is not empty and first item is dict
        if invalid_rows and not isinstance(invalid_rows[0], dict):
            raise ValueError("Invalid rows data must be dictionaries")
        self._invalid_rows = invalid_rows

    def export_word(self):
        """
        Export the valid and invalid attendance rows to a Word document.
        
        Returns: str: The file path of the generated Word document
            
        Raises IOError: If the Word document cannot be created or saved
        Raises ValueError: If the data format is invalid for Word export
        """
        ...


