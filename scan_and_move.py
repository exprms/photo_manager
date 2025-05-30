import os
import shutil
import sys
import argparse
import time

# usage:
# python scan_and_move.py <source-dir> <dest-dir> <year-to-move>

def move_files_by_year(source_dir, dest_dir, target_year):
    # Ensure destination directory exists
    os.makedirs(dest_dir, exist_ok=True)
    
    for root, _, files in os.walk(source_dir):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                # Get the modification time of the file
                mtime = os.path.getmtime(file_path)
                year = time.strftime('%Y', time.localtime(mtime))
                if year == target_year:
                    # Move the file
                    print(filename)
                    shutil.move(file_path, os.path.join(dest_dir, filename))
            except Exception:
                # Ignore errors
                pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Move files from a specific year.')
    parser.add_argument('source', help='Source directory')
    parser.add_argument('destination', help='Destination directory')
    parser.add_argument('year', help='Year to filter by (e.g., 2021)')

    args = parser.parse_args()

    move_files_by_year(args.source, args.destination, args.year)
