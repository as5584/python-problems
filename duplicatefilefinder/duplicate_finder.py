import os
import hashlib

PROJECT_FOLDER = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.join(PROJECT_FOLDER, "sample_files")


def get_hash(file_path):
    """Return SHA-256 hash of the file."""
    try:
        with open(file_path, "rb") as file:
            content = file.read()
        return hashlib.sha256(content).hexdigest()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


def main():
    print("DUPLICATE FILE FINDER")
    print(f"Scanning folder: {FOLDER}")
    print("-" * 60)

    if not os.path.exists(FOLDER):
        print("❌ Folder not found!")
        return

    hash_groups = {}   # hash -> list of relative paths
    file_list = []

    # Collect all files (skip .py files)
    for root, _, files in os.walk(FOLDER):
        for file_name in files:
            if file_name.endswith(".py"):
                continue
            full_path = os.path.join(root, file_name)
            file_list.append(full_path)

    total_files = len(file_list)
    print(f"Found {total_files} files to scan.\n")
    

  
    for i, full_path in enumerate(file_list):
        file_hash = get_hash(full_path)
        
        if file_hash:
            rel_path = os.path.relpath(full_path, FOLDER)
            if file_hash not in hash_groups:
                hash_groups[file_hash] = []
            hash_groups[file_hash].append(rel_path)

    # Show duplicate groups
    duplicates = []
    group_number = 1

    print("\n🔍 Duplicate Groups Found:")
    
    has_duplicates = False
    
    for files in hash_groups.values():
        if len(files) > 1:
            has_duplicates = True
            print(f"\nGroup {group_number}:")
            for name in files:
                print(f"   • {name}")
            duplicates.extend(files[1:])  # Mark all except first as duplicates
            group_number += 1

    if not has_duplicates:
        print("\n✅ No duplicate files found!")

    print("-" * 60)
    print("Scan complete.")

if __name__ == "__main__":
    main()
    