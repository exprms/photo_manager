import os
import sys
import argparse
import hashlib
import subprocess
import json
import sqlite3

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Scan directory for media files and extract metadata.")
parser.add_argument("root_dir", help="Root directory to scan")
parser.add_argument("--db", dest='db_enabled', action='store_true', help="Enable saving to SQLite database")
args = parser.parse_args()

ROOT_DIR = args.root_dir
DB_ENABLED = args.db_enabled

META_KEYS = [
    "SourceFile",
    "FileName",
    "Directory",
    "FileModifyDate",
    "FileTypeExtension",
    ]

# SQLite database file path
DB_PATH = "media_files.db"

def get_file_size(filepath):
    return os.path.getsize(filepath)

def extract_metadata(filepath):
    """Extract metadata using exiftool."""
    try:
        import subprocess
        cmd = ['exiftool', '-json', filepath]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"ExifTool error for {filepath}")
            return {}
        json_data = json.loads(result.stdout)
        metainfo = json_data[0]
        metadata = {}
        for key in META_KEYS:
            metadata.update({key: metainfo[key]})
        return metadata #json_data[0]
    except Exception as e:
        print(f"Error extracting metadata from {filepath}: {e}")
        return {}


def hash_file(filepath):
    """Compute SHA-256 hash."""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

def init_db():
    """Initialize SQLite database and table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS media_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            source_path TEXT,
            directory TEXT,
            filetype TEXT,       
            size_mb REAL,
            modified_date TEXT,
            year TEXT,
            month TEXT,
            hash TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(filename, source_path, directory, filetype, size, modified_date, file_hash):
    """Insert file info into SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO media_files (filename, source_path, directory, filetype, size_mb, modified_date, year, month, hash)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        filename,
        source_path,
        directory,
        filetype,
        size,
        modified_date,
        modified_date[0:4],
        modified_date[5:7],
        file_hash
    ))
    conn.commit()
    conn.close()

def compare_files(file1, file2):
    """Compare file hashes for equality."""
    hash1 = hash_file(file1)
    hash2 = hash_file(file2)
    return hash1 == hash2

def main():
    if DB_ENABLED:
        init_db()

    file_info_list = []

    for dirpath, dirnames, filenames in os.walk(ROOT_DIR):
        for filename in filenames:
            if filename.lower().endswith(('.jpg', '.jpeg', '.mp4')):
                filepath = os.path.join(dirpath, filename)
                print(f"Processing: {filepath}")

                size = round(get_file_size(filepath)/(1024*1024), 1)
                file_hash = hash_file(filepath)

                metadata = extract_metadata(filepath)
    
                file_info = {
                    "path": filepath,
                    "size": size,
                    "metadata": metadata['Directory'],
                    "hash": file_hash
                }
                file_info_list.append(file_info)

                if DB_ENABLED: 
                    save_to_db(
                        filename=metadata['FileName'], 
                        source_path=metadata['SourceFile'], 
                        directory=metadata['Directory'], 
                        filetype=metadata['FileTypeExtension'], 
                        size=size, 
                        modified_date=metadata['FileModifyDate'], 
                        file_hash=file_hash)
                else:
                    print(file_info_list)

if __name__ == "__main__":
    main()
