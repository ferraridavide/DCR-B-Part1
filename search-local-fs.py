
import os
import fnmatch

def find_files(starting_path, search_string):
    found_files = []
    for root, dirs, files in os.walk(starting_path):
        for file in files:
            
            file_path = os.path.join(root, file)
            # Check if the file name contains the search string
            if fnmatch.fnmatch(file, f'*{search_string}*'):
                found_files.append(("name", file_path))
                #print(f"Found file: {file_path}")
                continue
            # Check if the file content contains the search string
            if os.path.getsize(file_path) < 10*1024:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if search_string in content:
                        found_files.append(("content", file_path))
                        #print(f"Found file: {file_path}")

    return found_files

folder_path = os.getcwd()
print("Current directory:", folder_path)
file_pattern = input("Enter the file pattern: ")  # Change this to your desired file pattern

result = find_files(folder_path, file_pattern)
print("Files found:")
for reason, name in result:
    print(reason + " -> " + name)

