import os

def list_files_in_directory(directory):
    try:
        for root, _, files in os.walk(directory):
            for file in files:
                print(file)
    except Exception as e:
        print(f"An error occurred: {e}")

# Specify the directory
directory_path = r"D:\\wre\\The Merge\\game\\images\\bg"

list_files_in_directory(directory_path)
