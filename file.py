#!/usr/bin/env python3
"""
Downloads Folder Monitor
Monitors the Downloads folder and sends alerts when new files appear.
"""

import os
import time
import argparse
import csv
from pathlib import Path
from datetime import datetime

# Configuration
DOWNLOADS_PATH = Path.home() / "Downloads"
CHECK_INTERVAL = 2  # seconds
CSV_FILE = Path(__file__).parent / "data.csv"

def load_existing_files():
    """Load existing files from the Downloads folder."""
    try:
        return set(DOWNLOADS_PATH.iterdir())
    except FileNotFoundError:
        print(f"Error: Downloads folder not found at {DOWNLOADS_PATH}")
        return set()

def save_to_csv(new_files):
    """Save new file information to CSV."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Check if CSV file exists, if not create with headers
    file_exists = CSV_FILE.exists()

    try:
        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['timestamp', 'filename', 'filepath', 'size_bytes', 'size_mb', 'type', 'extension', 'file_category']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            for file_path in new_files:
                file_info = file_path.stat()
                size_bytes = file_info.st_size
                size_mb = round(size_bytes / (1024 * 1024), 2)
                file_type = 'Directory' if file_path.is_dir() else 'File'
                extension = file_path.suffix.lower()

                # Determine file category
                if extension in ['.dmg', '.pkg', '.zip', '.tar.gz', '.rar', '.7z']:
                    category = 'Installer/Archive'
                elif extension in ['.jpg', '.jpeg', '.png', '.gif', '.heic', '.bmp', '.svg']:
                    category = 'Image'
                elif extension in ['.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv']:
                    category = 'Video'
                elif extension in ['.csv', '.xlsx', '.xls', '.pdf', '.txt', '.doc', '.docx']:
                    category = 'Document'
                elif extension in ['.mp3', '.wav', '.flac', '.m4a', '.aac']:
                    category = 'Audio'
                else:
                    category = 'Other'

                writer.writerow({
                    'timestamp': timestamp,
                    'filename': file_path.name,
                    'filepath': str(file_path),
                    'size_bytes': size_bytes,
                    'size_mb': size_mb,
                    'type': file_type,
                    'extension': extension,
                    'file_category': category
                })

        print(f"📝 Saved {len(new_files)} new file(s) to {CSV_FILE}")

    except Exception as e:
        print(f"❌ Error saving to CSV: {e}")

def monitor_downloads(continuous=True):
    """Monitor the Downloads folder for new files."""
    print(f"📁 Monitoring Downloads folder: {DOWNLOADS_PATH}")
    print(f"⏱️  Check interval: {CHECK_INTERVAL} seconds")
    print("Press Ctrl+C to stop monitoring...\n")

    # Get initial state
    existing_files = load_existing_files()
    print(f"✅ Found {len(existing_files)} existing files/folders")

    try:
        while True:
            time.sleep(CHECK_INTERVAL)
            current_files = load_existing_files()

            # Find new files
            new_files = current_files - existing_files

            if new_files:
                save_to_csv(new_files)
                existing_files.update(new_files)

            if not continuous:
                break

    except KeyboardInterrupt:
        print("\n👋 Monitoring stopped.")

def check_once():
    """Check once for new files and exit."""
    existing_files = load_existing_files()
    print(f"📁 Current files in Downloads: {len(existing_files)}")
    print("Monitoring for new files for 10 seconds...")

    time.sleep(10)

    current_files = load_existing_files()
    new_files = current_files - existing_files

    if new_files:
        save_to_csv(new_files)
    else:
        print("✅ No new files detected.")

def main():
    global CHECK_INTERVAL
    parser = argparse.ArgumentParser(description="Monitor Downloads folder for new files")
    parser.add_argument("--once", action="store_true",
                       help="Check once and exit (useful for testing)")
    parser.add_argument("--interval", type=int, default=CHECK_INTERVAL,
                       help=f"Check interval in seconds (default: {CHECK_INTERVAL})")

    args = parser.parse_args()

    CHECK_INTERVAL = args.interval

    if args.once:
        check_once()
    else:
        monitor_downloads(continuous=True)

if __name__ == "__main__":
    main()