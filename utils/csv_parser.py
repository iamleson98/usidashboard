import os
import pandas as pd


class CheckingEventParser(object):
    def __init__(self, file_path: str):
        if not os.path.exists(file_path):
            raise Exception(f"path to file {file_path} does not exist")
        
        self.file_path = file_path

        try:
            # first 7 rows contains un-related information
            self.data_frame = pd.read_excel(io=self.file_path, sheet_name="Sheet1", skiprows=0, engine='openpyxl')

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

