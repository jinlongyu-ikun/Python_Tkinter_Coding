# author jinyunlong
# createtime 2023/4/28 10:04
# 职业 锅炉房保安

import os
import random
import datetime
from pathlib import Path

def generate_random_directory_structure(root_dir, depth, max_dirs, max_files):
    if depth <= 0:
        return

    for _ in range(random.randint(1, max_dirs)):
        new_dir = Path(root_dir).joinpath(f"dir_{random.randint(1, 100000)}")
        os.makedirs(new_dir, exist_ok=True)

        generate_random_directory_structure(new_dir, depth-1, max_dirs, max_files)

        for _ in range(random.randint(1, max_files)):
            new_file = new_dir.joinpath(f"file_{random.randint(1, 100000)}.txt")
            with open(new_file, "w") as f:
                f.write("Sample content")

            random_days = random.randint(1, 30)
            random_date = datetime.datetime.now() - datetime.timedelta(days=random_days)
            timestamp = random_date.timestamp()
            os.utime(new_file, (timestamp, timestamp))

def main():
    root_dir = r'D:\Pycharm\PyCharm Community Edition 2020.3.3\workspace\delete_folder\folder'  # Set the root folder path here
    depth = 3  # Set the maximum depth of subdirectories
    max_dirs = 5  # Set the maximum number of subdirectories per directory
    max_files = 10  # Set the maximum number of files per directory

    generate_random_directory_structure(root_dir, depth, max_dirs, max_files)
    print("Random directory structure and files generated.")

if __name__ == '__main__':
    main()