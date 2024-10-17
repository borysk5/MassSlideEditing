import tkinter as tk
from tkinter import filedialog
from PIL import Image

def upload_single_file():
    global watermark_path
    watermark_path = filedialog.askopenfilename()
    if watermark_path:
        single_file_label.config(text="Watermark: " + watermark_path)

def upload_multiple_files():
    global files_to_process
    files_to_process = filedialog.askopenfilenames()
    if files_to_process:
        multiple_files_label.config(text="Files to Process: " + ', '.join(files_to_process))

def apply_watermark():
    if watermark_path and files_to_process:
        for file_path in files_to_process:
            image = Image.open(file_path)
            watermark = Image.open(watermark_path)
            image.paste(watermark, (0, 0), watermark)
            image.save(file_path)
        result_label.config(text="Watermark applied to files successfully.")

# Create the main window
root = tk.Tk()
root.title("File Uploader and Watermarker")

# Create and position the buttons
single_button = tk.Button(root, text="Upload Watermark", command=upload_single_file)
single_button.pack(pady=10)

multiple_button = tk.Button(root, text="Upload Files to Watermark", command=upload_multiple_files)
multiple_button.pack(pady=10)

process_button = tk.Button(root, text="Process Watermark", command=apply_watermark)
process_button.pack(pady=10)

# Labels to display the file paths
single_file_label = tk.Label(root, text="Watermark: ")
single_file_label.pack()

multiple_files_label = tk.Label(root, text="Files to Process: ")
multiple_files_label.pack()

result_label = tk.Label(root, text="")
result_label.pack()

# Global variables
watermark_path = None
files_to_process = []

# Run the application
root.mainloop()
