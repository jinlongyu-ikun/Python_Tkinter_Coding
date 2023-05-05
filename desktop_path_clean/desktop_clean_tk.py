# author jinyunlong
# createtime 2023/5/5 14:18
# 职业 锅炉房保安

import os
import random
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk


def generate_random_files(suffix, num_files, folder_path=None):
    if folder_path is None:
        folder_path = os.path.join(Path.home(), "Desktop")

    for i in range(num_files):
        file_name = f"test_file_{i}.{suffix}"
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "w") as f:
            f.write(f"This is test file {i} with suffix {suffix}")

    return f"Generated {num_files} files with the suffix '{suffix}' in the folder '{folder_path}'."

def archive_files_by_suffix(suffix, base_path=None):
    if base_path is None:
        base_path = os.path.join(Path.home(), "Desktop")

    files = os.listdir(base_path)

    matching_files = [file for file in files if file.endswith(suffix)]

    if not matching_files:
        return f"No files found with the suffix '{suffix}' in the folder '{base_path}'."

    archive_folder = os.path.join(base_path, f"Archived_{suffix}")
    os.makedirs(archive_folder, exist_ok=True)

    for file in matching_files:
        src_path = os.path.join(base_path, file)
        dst_path = os.path.join(archive_folder, file)
        shutil.move(src_path, dst_path)

    return f"Archived {len(matching_files)} files with the suffix '{suffix}' into the folder '{archive_folder}'."

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("File Archiver and Generator")
        self.geometry("400x400")

        # Improve appearance using ttk widgets and styles
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", 12))
        self.style.configure("TEntry", font=("Arial", 12), padx=5, pady=5)
        self.style.configure("TButton", font=("Arial", 12), padx=10, pady=5)

        self.create_widgets()

    def create_widgets(self):
        self.archive_label = ttk.Label(self, text="Archive files by suffix")
        self.archive_label.pack(pady=10)

        self.suffix_entry = ttk.Entry(self)
        self.suffix_entry.pack(pady=5)
        self.suffix_entry.insert(0, "Enter file suffix")

        self.folder_entry = ttk.Entry(self)
        self.folder_entry.pack(pady=5)
        self.folder_entry.insert(0, os.path.join(Path.home(), "Desktop"))

        self.archive_button = ttk.Button(self, text="Archive Files", command=self.archive_files)
        self.archive_button.pack(pady=10)

        self.generate_label = ttk.Label(self, text="Generate random files")
        self.generate_label.pack(pady=10)

        self.gen_suffix_entry = ttk.Entry(self)
        self.gen_suffix_entry.pack(pady=5)
        self.gen_suffix_entry.insert(0, "Enter file suffix")

        self.gen_folder_entry = ttk.Entry(self)
        self.gen_folder_entry.pack(pady=5)
        self.gen_folder_entry.insert(0, os.path.join(Path.home(), "Desktop"))

        self.generate_button = ttk.Button(self, text="Generate Files", command=self.generate_files)
        self.generate_button.pack(pady=10)

    def archive_files(self):
        suffix = self.suffix_entry.get()
        folder_path = self.folder_entry.get().strip()
        if not folder_path:
            result = archive_files_by_suffix(suffix)
        else:
            result = archive_files_by_suffix(suffix, base_path=folder_path)
        messagebox.showinfo("Result", result)

    def generate_files(self):
        suffix = self.gen_suffix_entry.get()
        folder_path = self.gen_folder_entry.get().strip()

        if not folder_path:
            folder_path = None

        num_files = random.randint(1, 10)
        result = generate_random_files(suffix, num_files, folder_path=folder_path)
        messagebox.showinfo("Result", result)

if __name__ == "__main__":
    app = Application()
    app.mainloop()

