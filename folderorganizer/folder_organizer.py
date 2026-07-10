import os
import shutil

PROJECT_FOLDER = os.path.dirname(os.path.abspath(__file__))
MESSY_FOLDER = os.path.join(PROJECT_FOLDER, "messy_files")


FILE_TYPES = {
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".pdf": "Documents",
    ".txt": "Documents",
    ".doc": "Documents",
    ".mp4": "Videos",
    ".avi": "Videos",
    ".zip": "Archives",
    ".rar": "Archives",
}


def main():
    print("FOLDER ORGANIZER")
    print("Project folder:", PROJECT_FOLDER)
    os.makedirs(MESSY_FOLDER, exist_ok=True)

    files = [
        os.path.join(MESSY_FOLDER, f)
        for f in os.listdir(MESSY_FOLDER)
        if os.path.isfile(os.path.join(MESSY_FOLDER, f))
    ]

    if not files:
        print("No files in messy_files folder. Please add files to organize.")
        return

    moved = 0
    skipped = 0

    for file_path in files:
        ext = os.path.splitext(file_path)[1].lower()
        folder_name = FILE_TYPES.get(ext)

        if folder_name is None:
            print("Skipped:", os.path.basename(file_path))
            skipped += 1
            continue

        target_folder = os.path.join(PROJECT_FOLDER, folder_name)
        os.makedirs(target_folder, exist_ok=True)

        target_path = os.path.join(target_folder, os.path.basename(file_path))
        
        if os.path.exists(target_path):
            print(f"Skipped (file exists): {os.path.basename(file_path)}")
            skipped += 1
            continue
            
        shutil.move(file_path, target_path)
        print(f"Moved: {os.path.basename(file_path)} -> {folder_name}/")
        moved += 1

    print("-" * 40)
    print(f"Done! Moved {moved} file(s), skipped {skipped} file(s).")


if __name__ == "__main__":
    main()