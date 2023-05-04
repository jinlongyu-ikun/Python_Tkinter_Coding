# author jinyunlong
# createtime 2023/4/28 10:23
# 职业 锅炉房保安

import os
import shutil
import datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox


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


def backup_and_delete():
    root_dir = folder_path.get()
    days_diff = int(days_entry.get())
    target_date = datetime.datetime.now() - datetime.timedelta(days=days_diff)
    files_to_backup = get_files_before_date(root_dir, target_date)

    if files_to_backup:
        backup_files(root_dir, files_to_backup, days_diff)
        messagebox.showinfo("Success", f"Backup completed for {len(files_to_backup)} files.")
    else:
        messagebox.showwarning("No Files Found", "No files found before the specified date.")


def browse_folder():
    folder = filedialog.askdirectory()
    folder_path.set(folder)


app = tk.Tk()
app.title("Backup Files")

folder_path = tk.StringVar()

folder_label = tk.Label(app, text="Folder Path:")
folder_label.grid(row=0, column=0, padx=5, pady=5)

folder_entry = tk.Entry(app, textvariable=folder_path)
folder_entry.grid(row=0, column=1, padx=5, pady=5)

browse_button = tk.Button(app, text="Browse", command=browse_folder)
browse_button.grid(row=0, column=2, padx=5, pady=5)

days_label = tk.Label(app, text="Days:")
days_label.grid(row=1, column=0, padx=5, pady=5)

days_entry = tk.Entry(app)
days_entry.grid(row=1, column=1, padx=5, pady=5)

submit_button = tk.Button(app, text="Backup and Delete", command=backup_and_delete)
submit_button.grid(row=2, columnspan=3, padx=5, pady=5)

app.mainloop()