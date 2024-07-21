import os
import pandas as pd

FILE_NAME = "htx_clothing_stores.csv"

def getFileDir(file_name):
    working_dir = os.getcwd()
    source_dir = os.path.join(working_dir, "source")
    file_dir = os.path.join(source_dir, "support_files")

    return os.path.join(file_dir, file_name)

def removeDuplicates():
    file_path = getFileDir(FILE_NAME)
    df = pd.read_csv(file_path, header=None, names=['col'])
    no_dups = df.drop_duplicates()
    no_dups.to_csv(file_path, index=False, header=False)

def main():
    removeDuplicates()

