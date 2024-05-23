import os
import mysql.connector

def discover_files_and_directories(start_path):
    directories = {}
    files = []

    for root, dirs, filenames in os.walk(start_path):
        parent_dir = os.path.basename(root)
        parent_path = os.path.dirname(root)
        parent_id = directories.get(parent_path, 1)

        directories[root] = parent_id

        for filename in filenames:
            file_path = os.path.join(root, filename)
            files.append((filename, root))

    return directories, files

def insert_directories(cursor, directories):
    directory_id_map = {}
    for path, dir_id in directories.items():
        parent_path = os.path.dirname(path)
        parent_id = directory_id_map.get(parent_path, 1) # Default to root
        cursor.execute(
            "INSERT INTO directory (name, parent) VALUES (%s, %s)",
            (os.path.basename(path), parent_id)
        )
        directory_id_map[path] = cursor.lastrowid
    return directory_id_map

def insert_files(cursor, files):
    cursor.executemany(
        "INSERT INTO file (name, directory_id, content, searchable) VALUES (%s, %s, %s, %s)",
        files
    )

def is_searchable(dir_path, filename):
    if filename.endswith(".txt") or filename.endswith(".html") or filename.endswith(".md"):
        with open(os.path.join(dir_path, filename), "r", encoding="utf-8") as f:
            return (f.read(), True)
    else:
        return (None, False)

def main(start_path):
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="my-secret-pw",
        database="dcr"
    )
    cursor = cnx.cursor()

    directories, files = discover_files_and_directories(start_path)

    directory_id_map = insert_directories(cursor, directories)

    files_with_ids = [(name, directory_id_map[dir_path], content, searchable) 
                  for name, dir_path in files 
                  for content, searchable in (is_searchable(dir_path, name),) 
                  if content is not None or searchable is False]
    insert_files(cursor, files_with_ids)

    cnx.commit()


    cursor.close()
    cnx.close()

if __name__ == "__main__":
    start_path = rf"C:\Users\Davide\Documents\Trash\Dogsitter\Aprile-20240415T175944Z-001\Aprile"
    main(start_path)