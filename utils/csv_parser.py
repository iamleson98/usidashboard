import csv
import os
import pandas as pd

PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_FOLDER_NAME = "data"
DATA_DIR = os.path.join(PARENT_DIR, DATA_FOLDER_NAME)


class CheckingEventParser(object):
    def __init__(self, file_name: str):
        file_path = os.path.join(DATA_DIR, file_name)
        if not os.path.exists(file_path):
            raise Exception(f"path to file {file_name} does not exist")

        try:
            dframe = pd.read_csv(filepath_or_buffer=file_path, sep=",", encoding="utf-8")
            # data_content = open(file_path, 'r', encoding="utf-8")
            # # print(data_content.read())
            # csv_content = csv.reader(data_content)
            # # # print(csv_content)
            # for row in csv_content:
            #     print(row)
            print(dframe.head(10))

        except Exception as e:
            raise Exception(f"Failed to read content of file {file_path}. Error; {e}")
        # finally:
        #     data_content.close()


CheckingEventParser(file_name="Identity Access Search_2025_04_23_13_09_39_620.csv")
