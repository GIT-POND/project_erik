import os
import sys
import time
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

# def main():
#     removeDuplicates()

def print_loading_bar(iteration, total, prefix='', suffix='', length=50, fill='█'):
    """
    Call in a loop to create a terminal progress bar.
    
    Parameters:
    iteration (int): current iteration (required)
    total (int): total iterations (required)
    prefix (str): prefix string (optional)
    suffix (str): suffix string (optional)
    length (int): character length of bar (optional, default: 50)
    fill (str): bar fill character (optional, default: '█')
    """
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()


