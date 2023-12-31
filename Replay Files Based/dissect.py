import tkinter as tk
from tkinter import filedialog
import os

# # Create the Tkinter window
# root = tk.Tk()
# root.withdraw()  # Hide the main window

# # Open a file picker dialog
# file_path = filedialog.askopenfilename(filetypes=[("REC files", "*.rec")])

file_path = "C:/Program Files (x86)/Steam/steamapps/common/Tom Clancy's Rainbow Six Siege/MatchReplay/Match-2023-12-30_10-49-38-115/Match-2023-12-30_10-49-38-115-R01.rec"

file_name = os.path.splitext(os.path.basename(file_path))[0]

# Splitting the filename by '-' and getting the last part
last_part = file_name.split('-')[-1]


if file_path:
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        data = file.read()
        data = data.replace('\x00', '-')
        data = ''.join(
            '[{}]'.format(c) if ord(c) < 32 else c for c in data
        )

    output_file_path = f'{file_name}_out.txt'

    # Writing the decoded text to a file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(data)

    print(f"Decoded text has been saved to {output_file_path}")
else:
    print("No file selected")
