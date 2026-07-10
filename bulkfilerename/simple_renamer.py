import os
import re
import shutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = os.path.join(SCRIPT_DIR, "input_files")
OUTPUT_FOLDER = os.path.join(SCRIPT_DIR, "output_files")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def clean_filename(name):
    name = name.replace(" ", "_")
    name = re.sub(r"[^\w\-.]", "", name)
    name = re.sub(r"_+", "_", name)
    return name.strip("_")


files = []

for file in os.listdir(INPUT_FOLDER):
    file_path = os.path.join(INPUT_FOLDER, file)

    if os.path.isfile(file_path):
        files.append(file_path)

files.sort()


count = 1

for file_path in files:
    filename = os.path.basename(file_path)
    name, ext = os.path.splitext(filename)

    new_name = f"document_{count:03d}_{clean_filename(name)}{ext.lower()}"

    destination = os.path.join(OUTPUT_FOLDER, new_name)

    shutil.copy2(file_path, destination)

    print(f"{filename}  -->  {new_name}")

    count += 1

print("\nAll files renamed and copied successfully!")