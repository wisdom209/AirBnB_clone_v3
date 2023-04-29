import os
import argparse

def print_directory_structure(path, indent=''):
    """
    Prints the folder and file structure of a directory recursively.

    Args:
        path (str): The path to the root directory.
        indent (str): The indentation string.
    """
    for item in os.listdir(path):
        item_path = os.path.join(path, item)

        # Check if the item is a file or a directory
        if os.path.isfile(item_path):
            print(indent + '- ' + item)
        elif os.path.isdir(item_path):
            print(indent + '+ ' + item)
            print_directory_structure(item_path, indent=indent + '  ')

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('path', type=str, help='The path to the root directory')
args = parser.parse_args()

# Print the directory structure
print_directory_structure(args.path)
