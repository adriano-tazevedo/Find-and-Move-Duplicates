import hashlib
import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def hash_file(filename):
    """Calculate the SHA-1 hash of a file."""
    h = hashlib.sha1()
    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def check_for_duplicates(path):
    """Return a list of duplicate files in the directory tree starting from path."""
    files_seen = {}
    duplicates = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_hash = hash_file(file_path)
            if file_hash in files_seen:
                if os.path.isfile(file_path) and file_path != files_seen[file_hash]:
                    duplicates.append(file_path)
            else:
                files_seen[file_hash] = file_path
    return duplicates

def move_duplicates(src, dst, duplicates):
    """Move duplicate files from src to dst."""
    for file_path in duplicates:
        dst_file_path = os.path.join(dst, os.path.relpath(file_path, src))
        dst_dir = os.path.dirname(dst_file_path)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        shutil.move(file_path, dst_file_path)

def choose_directory(title):
    """Open a file dialog to choose a directory."""
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory(title=title)

def find_duplicates():
    """Find duplicates and move them to the destination directory."""
    src = choose_directory("Choose source directory")
    dst = choose_directory("Choose destination directory")
    duplicates = check_for_duplicates(src)
    move_duplicates(src, dst, duplicates)
    messagebox.showinfo("Done", "Duplicates moved to " + dst)

def quit_app():
    """Quit the application."""
    root.destroy()

# Create GUI
root = tk.Tk()
root.title("Find and Move Duplicates")

button_find = tk.Button(root, text="Find and Move Duplicates", command=find_duplicates)
button_find.pack()

button_quit = tk.Button(root, text="Quit", command=quit_app)
button_quit.pack()

root.mainloop()
