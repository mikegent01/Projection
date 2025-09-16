import os
import shutil

def organize_assets_in_place(work_dir):
    """
    Organizes game assets within a specified 'work_dir' into categorized subdirectories.
    Files will be moved from the root of work_dir into its subfolders.
    """

    # Define target subdirectories and their keywords.
    # Files will be moved to the FIRST matching category.
    # Order matters: more specific classifications or more important categories should come first.
    categories = {
        "source_files": [".aseprite", ".psd"],  # Editable project files
        "docs": [".txt"],  # Text documents
        "animated": [".gif"], # Animated sprites/backgrounds

        "palettes": ["color palette", "palette", "china", "4362afr"],  # Specific palette names/keywords

        "characters": ["ben", "sargent", "drill", "milfe", "mint", "smolben", "pope", "pencilman", "deer"],
        "backgrounds": ["background", "scene", "stage", "floor", "walkaway"],
        "ui": ["speechbubble", "title"],  # Big Title Redone.png will match "title"
        "items": ["projector", "podium"],
        "monsters": [],  # 'deer' is in 'characters' for now; populate if you have distinct monster files
        "fx": ["burn", "eye"],  # 'eye.aseprite' could be an eye glint effect
        "sprites_generic": ["sprite-"], # For generic sprites like Sprite-0001
        "misc": ["screenshot", "prototype", "work", "unplug"]  # Catch-all for less specific or temporary files
    }

    print(f"Starting internal organization of '{work_dir}'...")

    # Create all subdirectories within the work_dir
    for subdir_name in categories:
        os.makedirs(os.path.join(work_dir, subdir_name), exist_ok=True)
    # Ensure an 'unclassified' directory exists for unmatched files
    os.makedirs(os.path.join(work_dir, "unclassified"), exist_ok=True)


    # --- Iterate through each file in the work directory ---
    # List files, but we need to be careful not to try and move newly created subdirectories
    # So, list only files first, before any moves happen.
    files_to_organize = [f for f in os.listdir(work_dir) if os.path.isfile(os.path.join(work_dir, f))]

    for filename in files_to_organize:
        source_path = os.path.join(work_dir, filename)

        # Prepare for classification
        destination_subdir = "unclassified"  # Default if no category matches
        lower_filename = filename.lower()
        file_extension = os.path.splitext(lower_filename)[1]  # e.g., ".png", ".aseprite"

        # --- Classification Logic ---
        for category, keywords in categories.items():
            matched = False

            # Handle categories based on file extension
            if category in ["source_files", "docs", "animated"]:
                if file_extension in keywords:
                    destination_subdir = category
                    matched = True
            # Handle keyword-based categories (checking if any keyword is in the filename)
            else:
                if any(k in lower_filename for k in keywords):
                    destination_subdir = category
                    matched = True
            
            if matched:
                break  # Stop after the first match

        # --- Move the file ---
        destination_dir = os.path.join(work_dir, destination_subdir)
        destination_path = os.path.join(destination_dir, filename)

        try:
            # Check if destination exists. If it does, and we don't want to overwrite, skip.
            # If you want to force overwrite, add os.remove(destination_path) before shutil.move
            if os.path.exists(destination_path):
                print(f"Skipping '{filename}': File already exists in '{destination_subdir}/'.")
                continue # Skip moving if file exists and we don't force overwrite

            shutil.move(source_path, destination_path)
            print(f"Moved: '{filename}' to '{destination_subdir}/'")
        except shutil.Error as e:
            print(f"Error moving '{filename}': {e}. Check permissions or if source/destination are on different filesystems.")
        except Exception as e:
            print(f"Unexpected error with '{filename}': {e}")

# --- Configuration ---
# !!! IMPORTANT: VERIFY THIS PATH IS CORRECT FOR YOUR SYSTEM !!!
# The specific folder you want to organize internally
EIGHT_BIT_WORK_FOLDER = r"D:\wre\Projection\game\images\8bitwork" 

# --- Run the Organization ---
if __name__ == "__main__":
    organize_assets_in_place(EIGHT_BIT_WORK_FOLDER)
    print("Organization complete.")