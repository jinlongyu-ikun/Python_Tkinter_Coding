# author jinyunlong
# createtime 2023/4/28 10:05
# 职业 锅炉房保安

import os
import shutil
import datetime
from pathlib import Path


def get_files_before_date(root_dir, target_date):
    files_to_backup = []

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))

            if file_mtime < target_date:
                files_to_backup.append(file_path)

    return files_to_backup


def backup_files(root_dir, files_to_backup, days_diff):
    backup_root = Path(root_dir).parent.joinpath(f"{Path(root_dir).name}_{days_diff}days")

    for file_path in files_to_backup:
        file_rel_path = os.path.relpath(file_path, root_dir)
        backup_file_path = backup_root.joinpath(file_rel_path)
        backup_file_dir = backup_file_path.parent

        if not backup_file_dir.exists():
            os.makedirs(backup_file_dir)

        shutil.copy(file_path, backup_file_path)
        os.remove(file_path)


def main():
    root_dir = r'D:\Pycharm\PyCharm Community Edition 2020.3.3\workspace\delete_folder\folder'
    days_diff = 10  # set the x days difference here
    target_date = datetime.datetime.now() - datetime.timedelta(days=days_diff)
    files_to_backup = get_files_before_date(root_dir, target_date)

    if files_to_backup:
        backup_files(root_dir, files_to_backup, days_diff)
        print(f"Backup completed for {len(files_to_backup)} files.")
    else:
        print("No files found before the specified date.")


if __name__ == '__main__':
    main()

