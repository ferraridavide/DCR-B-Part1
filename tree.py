import mysql.connector
from mysql.connector import Error

def fetch_data(cursor):
    # Leggi le cartelle
    cursor.execute("SELECT id, name, parent FROM directory")
    directories = cursor.fetchall()

    # Leggi tutti i file
    cursor.execute("SELECT id, name, directory_id FROM file")
    files = cursor.fetchall()

    return directories, files

def build_tree(directories, files):
    tree = {}
    directory_map = {directory[0]: {'id': directory[0], 'name': directory[1], 'parent': directory[2], 'subdirectories': {}, 'files': []} for directory in directories}

    for directory in directories:
        directory_id, directory_name, parent_id = directory
        if parent_id is None:
            tree[directory_id] = directory_map[directory_id]

    for directory_id, directory in directory_map.items():
        parent_id = directory['parent']
        if parent_id is not None and parent_id in directory_map:
            directory_map[parent_id]['subdirectories'][directory_id] = directory

    for file in files:
        file_id, file_name, directory_id = file
        if directory_id in directory_map:
            directory_map[directory_id]['files'].append({'id': file_id, 'name': file_name})

    return tree

def print_tree(tree, level=0):
    for directory_id, directory in tree.items():
        print('    ' * level + f"📁 {directory['name']}")
        for file in directory['files']:
            print('    ' * (level + 1) + f"📄 {file['name']}")
        print_tree(directory['subdirectories'], level + 1)


def main():
    
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="my-secret-pw",
        database="dcr"
    )

    if connection.is_connected():
        cursor = connection.cursor()
        directories, files = fetch_data(cursor)
        tree = build_tree(directories, files)
        print_tree(tree)


    if connection.is_connected():
        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()