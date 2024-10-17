#!/usr/bin/env python

from gimpfu import *
import os
import gtk

LAST_DIR_FILE = os.path.expanduser("~/.gimp_last_directory.txt")  # File to store the last opened directory

def get_last_directory():
    """Retrieve the last used directory from a file."""
    if os.path.exists(LAST_DIR_FILE):
        with open(LAST_DIR_FILE, 'r') as f:
            last_dir = f.read().strip()
            if os.path.isdir(last_dir):
                return last_dir
    return None

def save_last_directory(directory):
    """Save the last used directory to a file."""
    with open(LAST_DIR_FILE, 'w') as f:
        f.write(directory)

def apply_watermark(image, drawable):
    # Create a file chooser dialog
    dialog = gtk.FileChooserDialog(
        "Select images to watermark",
        None,
        gtk.FILE_CHOOSER_ACTION_OPEN,
        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK)
    )
    dialog.set_select_multiple(True)

    # Add file filters
    filter_images = gtk.FileFilter()
    filter_images.set_name("Image files")
    filter_images.add_mime_type("image/png")
    filter_images.add_mime_type("image/jpeg")
    filter_images.add_pattern("*.png")
    filter_images.add_pattern("*.jpg")
    filter_images.add_pattern("*.jpeg")
    dialog.add_filter(filter_images)

    # Set the dialog to open in the last used directory, if available
    last_directory = get_last_directory()
    if last_directory:
        dialog.set_current_folder(last_directory)

    # Show the dialog and get the selected files
    response = dialog.run()
    if response == gtk.RESPONSE_OK:
        files_to_process = dialog.get_filenames()
        if files_to_process:
            # Save the directory of the first selected file as the last used directory
            save_last_directory(os.path.dirname(files_to_process[0]))
    else:
        dialog.destroy()
        return

    dialog.destroy()

    if not files_to_process:
        return

    # Get the current image as watermark
    watermark = pdb.gimp_image_duplicate(image)

    # Process each selected file
    for file_path in files_to_process:
        # Open the image
        target_image = pdb.gimp_file_load(file_path, file_path)
        target_layer = pdb.gimp_image_get_active_layer(target_image)

        # Resize watermark to match target image size
        pdb.gimp_image_scale(watermark, target_image.width, target_image.height)

        # Copy watermark to target image
        watermark_layer = pdb.gimp_layer_new_from_drawable(pdb.gimp_image_get_active_layer(watermark), target_image)
        pdb.gimp_image_insert_layer(target_image, watermark_layer, None, 0)

        # Merge down
        merged_layer = pdb.gimp_image_merge_down(target_image, watermark_layer, CLIP_TO_IMAGE)

        # Save the image
        output_path = file_path  # os.path.splitext(file_path)[0] + "_watermarked.png"
        pdb.gimp_file_save(target_image, merged_layer, output_path, output_path)

        # Close the image
        pdb.gimp_image_delete(target_image)

    # Clean up
    pdb.gimp_image_delete(watermark)

    pdb.gimp_message("Watermark applied to all selected images.")

register(
    "python-fu-batch-watermark",
    "Apply current image as watermark to multiple images",
    "Applies the current image as a watermark to multiple selected images",
    "Your Name",
    "Your Name",
    "2023",
    "<Image>/File/Apply Watermark...",
    "*",
    [],
    [],
    apply_watermark
)

main()
