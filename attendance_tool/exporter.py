import docx, docx.shared


class Exporter:
    # Constructor with valid and invalid rows, and the document's title
    def __init__(self, valid_rows, invalid_rows, title="Attendance Report"):
        self.valid_rows = valid_rows
        self.invalid_rows = invalid_rows
        self.title = title

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

    # Getter for title
    @property
    def title(self):
        return self._title

    # Setter for title
    @title.setter
    def title(self, title):
        if not isinstance(title, str):
            raise ValueError("Title must be a string")
        if not title.strip():
            raise ValueError("Title cannot be empty")
        self._title = title

    def export_word(self):
        """
        Export the valid and invalid attendance rows to a Word document.

        Returns: str: The file path of the generated Word document

        Raises PermissionError: If the Word document cannot be created or saved
        """
        # Intialize Document
        document = docx.Document()

        # Set default font for the document
        # style = document.styles['Normal']
        # font = style.font
        # font.name = 'Arial'
        # font.size = docx.shared.Pt(21)
        # font.color.rgb = docx.shared.RGBColor(0, 0, 0)  # Black color

        # Add heading
        heading = document.add_heading(
            f"{self.title} - Microsoft Students Partners Club (MSP)"
        )

        #  Style the heading
        heading_run = heading.runs[0]  # .runs[0] = first text chunk in the heading that we can style
        heading_run.font.name = "Arial"  # Change font family to Arial
        heading_run.font.size = docx.shared.Pt(21)  # Set font size to 21 points
        heading_run.font.color.rgb = docx.shared.RGBColor(
            0, 0, 0
        )  # Set text color to black

        try:
            # Rename this title later to self.title or smth similiar
            document.save("demo.docx")
        except PermissionError as error:
            # Raised possibly because file is open, and we're trying to save it
            raise PermissionError(error)
