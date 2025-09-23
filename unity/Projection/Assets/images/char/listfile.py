import os

# Get the directory where this script is located
base_dir = os.path.dirname(os.path.abspath(__file__))

# Walk through all subdirectories and list files
for root, dirs, files in os.walk(base_dir):
    print(f"\nDirectory: {root}")
    for file in files:
        print(f"  - {file}")
