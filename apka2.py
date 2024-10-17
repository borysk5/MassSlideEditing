import tkinter as tk
from PIL import Image, ImageTk
import os

# Global variable for scale
scale = 0.6

x_toedit = 0
y_toedit = 0
leftimage = "2023.png"
rightimage = "2023.png"
currentcolor = (0,0,0)
oldcolor = (0,0,0)
trueorfalse = False

def print_confirmation():
    start_year = int(leftimage[:-4])
    end_year = int(rightimage[:-4])
    for year in range(start_year, end_year + 1):
        image_path = f"{year}.png"
        if os.path.exists(image_path):
            bucket_fill(image_path, x_toedit, y_toedit,oldcolor,currentcolor,trueorfalse)
        else:
            print(f"Image '{image_path}' not found.")
    print("Confirm")
    update_image(entry, image_labels["start"], "start")
    update_image(entry_start, image_labels["end"], "end")
    

def bucket_fill(image_path, x, y, old_color, replacement_color,override):
    """
    Perform bucket fill operation on the image starting from coordinates (x, y)
    with the target_color, replacing it with replacement_color.
    """
    image = Image.open(image_path)
    width, height = image.size
    target_color = image.getpixel((x, y))
    if (target_color != old_color and override != 1):
        return
    if old_color == (0,0,0) or target_color == (0,0,0) or old_color == (197,255,254) or target_color == (197,255,254):
        return    
    stack = [(x, y)]
    while stack:
        current_x, current_y = stack.pop()
        if (0 <= current_x < width and 0 <= current_y < height and
            image.getpixel((current_x, current_y)) == target_color):
            image.putpixel((current_x, current_y), replacement_color)
            stack.extend([(current_x+1, current_y), (current_x-1, current_y),
                          (current_x, current_y+1), (current_x, current_y-1)])
    
    image.save(image_path)

# Function to handle image click event
def image_click(event, label):
    if event.num == 1:  # Left click
        x = event.x
        y = event.y
        # Convert coordinates to coordinates on the original image
        original_x = int(x / scale)
        original_y = int(y / scale)
        image = Image.open(rightimage)
        target_color = image.getpixel((original_x, original_y))
        global oldcolor
        oldcolor = target_color
        global x_toedit, y_toedit
        x_toedit = original_x
        y_toedit = original_y
        lx.delete(0, tk.END)
        lx.insert(0, x_toedit)
        ly.delete(0, tk.END)
        ly.insert(0, y_toedit)
        print(f"Clicked pixel coordinates on {label} image:", original_x, original_y)
    elif event.num == 3:  # Right click
        x = event.x
        y = event.y
        # Convert coordinates to coordinates on the original image
        original_x = int(x / scale)
        original_y = int(y / scale)
        print(leftimage)
        print(rightimage)
        image = Image.open(rightimage)
        target_color = image.getpixel((original_x, original_y))
        global currentcolor
        currentcolor = target_color
        global r_entry,g_entry,b_entry
        r_entry.delete(0, tk.END)
        r_entry.insert(0, target_color[0])
        g_entry.delete(0, tk.END)
        g_entry.insert(0, target_color[1])
        b_entry.delete(0, tk.END)
        b_entry.insert(0, target_color[2])
        print("done")

def update_l(entry, label):
        if label == "lx":
            global x_toedit
            x_toedit = int(entry.get())
        else:
            global y_toedit
            y_toedit = int(entry.get())
        image = Image.open(rightimage)
        target_color = image.getpixel((int(x_toedit),int(y_toedit)))
        global oldcolor
        oldcolor = target_color

# Function to update image preview
def update_image(entry, image_label, label):
    try:
        image_name = entry.get() + ".png"
        global currentimage
        if label == "start":
            global leftimage
            leftimage = image_name
        else:
            global rightimage
            rightimage = image_name
        image = Image.open(image_name)
        # Calculate new dimensions while maintaining aspect ratio
        width, height = image.size
        new_width = int(width * scale)
        new_height = int(height * scale)
        image = image.resize((new_width, new_height))
        photo = ImageTk.PhotoImage(image)
        image_label.configure(image=photo)
        image_label.image = photo
    except FileNotFoundError:
        # If the image file is not found, display a placeholder image
        placeholder_photo = ImageTk.PhotoImage(placeholder_image_resized)
        image_label.configure(image=placeholder_photo)
        image_label.image = placeholder_photo

# Function to toggle global variable value
def toggle_variable():
    global trueorfalse
    trueorfalse = not trueorfalse
    print("trueorfalse is now:", trueorfalse)

# Create main window
root = tk.Tk()
root.title("Image Preview")

canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar_y = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
canvas.configure(yscrollcommand=scrollbar_y.set)

# Add a scrollbar to the canvas
scrollbar = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=canvas.xview)
scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
canvas.configure(xscrollcommand=scrollbar.set)

# Create a frame to contain the widgets
frame = tk.Frame(canvas)
canvas.create_window((0,0), window=frame, anchor=tk.NW)


# Load placeholder image
placeholder_image = Image.open("2023.png")
placeholder_image_resized = placeholder_image.resize((int(placeholder_image.width * scale), int(placeholder_image.height * scale)))
placeholder_photo = ImageTk.PhotoImage(placeholder_image_resized)

# Create text field and label for first image name
entry_label = tk.Label(frame, text="Beginning")
entry_label.grid(row=0, column=0)
entry = tk.Entry(frame)
entry.grid(row=0, column=1)
entry.bind("<KeyRelease>", lambda event: update_image(entry, image_labels["start"], "start"))

# Create label and image viewer for first image
image_label_end = tk.Label(frame, image=placeholder_photo)
image_label_end.grid(row=1, column=0, columnspan=2)
image_label_end.bind("<Button-1>", lambda event: image_click(event, "start"))
image_label_end.bind("<Button-3>", lambda event: image_click(event, "start"))

# Create text fields and labels for color components
r_label = tk.Label(frame, text="r")
r_label.grid(row=2, column=0)
r_entry = tk.Entry(frame)
r_entry.grid(row=2, column=1)
r_entry.insert(0, "0")

g_label = tk.Label(frame, text="g")
g_label.grid(row=3, column=0)
g_entry = tk.Entry(frame)
g_entry.grid(row=3, column=1)
g_entry.insert(0, "0")

b_label = tk.Label(frame, text="b")
b_label.grid(row=4, column=0)
b_entry = tk.Entry(frame)
b_entry.grid(row=4, column=1)
b_entry.insert(0, "0")

lx = tk.Entry(frame)
lx.grid(row=2, column=2)
lx.bind("<KeyRelease>", lambda event: update_l(lx, "lx"))

ly = tk.Entry(frame)
ly.grid(row=2, column=3)
ly.bind("<KeyRelease>", lambda event: update_l(ly, "ly"))


# Create label and text field for second image name
entry_label_start = tk.Label(frame, text="Ending")
entry_label_start.grid(row=0, column=2)
entry_start = tk.Entry(frame)
entry_start.grid(row=0, column=3)
entry_start.bind("<KeyRelease>", lambda event: update_image(entry_start, image_labels["end"], "end"))

# Create label and image viewer for second image
image_label_start = tk.Label(frame, image=placeholder_photo)
image_label_start.grid(row=1, column=2, columnspan=2)
image_label_start.bind("<Button-1>", lambda event: image_click(event, "end"))
image_label_start.bind("<Button-3>", lambda event: image_click(event, "end"))

# Create checkbox button
checkbox_button = tk.Checkbutton(frame, text="Toggle", command=toggle_variable)
checkbox_button.grid(row=7, column=0, columnspan=2)


confirm_button = tk.Button(frame, text="Confirm", command=print_confirmation)
confirm_button.grid(row=5, column=0, columnspan=2)


frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Initialize image labels dictionary
image_labels = {"start": image_label_end, "end": image_label_start}
image_label_wrapper = {"end": canvas.create_window(0, 0, anchor=tk.NW), "start": canvas.create_window(0, 0, anchor=tk.NW)}


root.mainloop()
