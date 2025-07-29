import os, csv


class Processor:
    """
    __str__: Handles medium files (500-5,000 rows) perfectly fine for our use case
    """
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
        try:
            with open(self.file_path) as file:
                reader = csv.DictReader(file)

                rows = []
                for row in reader:
                    rows.append(str(row))
                
                if not rows:
                    return f"No data found in '{self.file_path}' file"
                
                # Join with newlines for readable output
                return '\n\n'.join(rows)  
        except FileNotFoundError:
            raise FileNotFoundError(f"Unable to open file: {self.file_path}")
        
