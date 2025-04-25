import os
import pandas as pd

PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_FOLDER_NAME = "data"
DATA_DIR = os.path.join(PARENT_DIR, DATA_FOLDER_NAME)


class CheckingEventParser(object):
    def __init__(self, file_name: str):
        self.file_path = os.path.join(DATA_DIR, file_name)
        if not os.path.exists(self.file_path):
            raise Exception(f"path to file {file_name} does not exist")

        try:
            # first 7 rows contains un-related information
            self.df = pd.read_excel(io=self.file_path, sheet_name="Sheet1", skiprows=0, engine='openpyxl')

        except Exception as e:
            raise Exception(f"Failed to read content of file {self.file_path}. Error; {e}")

    def logic_handle(self):
        pass

    def cleanup(self):
        """cleanup removes data files after use, to help save disk resource.
        Only call the method after you are done with data processing."""
        try:
            os.remove(self.file_path)
        except Exception as e:
            raise Exception(f"Failed to delete file: {self.file_path}")

