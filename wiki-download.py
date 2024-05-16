import sqlite3
import wikipediaapi
import os
import mysql.connector

wiki_wiki = wikipediaapi.Wikipedia('Digital_Content_Retrival_Ferrari/1.0 (davide.ferrari05@universitadipavia.it)', 'en', extract_format=wikipediaapi.ExtractFormat.WIKI)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="my-secret-pw",
  database="dcr"
)

print(mydb)


page_list = []

category_count = {}
page_count = {}


def create_directories(cursor, directory_names):
    current_parent_id = None
    directory_names = ["root"] + directory_names
    for directory_name in directory_names:
        if directory_name == "root":
            current_parent_id = 1
            continue
        if directory_name:
            cursor.execute("SELECT id FROM directory WHERE name = %s AND parent = %s", (directory_name, current_parent_id))
            result = cursor.fetchone()
            if result:
                current_parent_id = result[0]
            else:
                cursor.execute("INSERT INTO directory (name, parent) VALUES (%s, %s)", (directory_name, current_parent_id))
                current_parent_id = cursor.lastrowid
                mydb.commit()

def add_file(cursor, directory_path, filename, content):
    directory_path = ["root"] + directory_path
    cursor.execute("SELECT id FROM directory WHERE name = %s", (directory_path[-1],))
    result = cursor.fetchone()
    if result:
        directory_id = result[0]
    else:
        cursor.execute("INSERT INTO directory (name) VALUES (%s)", (directory_path[-1],))
        directory_id = cursor.lastrowid
        mydb.commit()

    cursor.execute("INSERT INTO file (name, directory_id, content) VALUES (%s, %s, %s)", (filename, directory_id, content))
    mydb.commit()
    print("File added successfully.")


def download_page(folders, page_title):
    path = os.path.join(os.getcwd(), *folders)

    # Create the folder structure
    os.makedirs(path, exist_ok=True)

    # File name and content
    filename = page_title + ".html"
    p_html = wiki_wiki.page(page_title)

    # Create the file inside the folder structure
    file_path = os.path.join(path, filename)
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(p_html.text)


def download_page_db(folders, page_title):
    # Create directories if they don't exist
    create_directories(cursor, folders)
    p_html = wiki_wiki.page(page_title)

    # Add file to the database
    add_file(cursor, folders, page_title, p_html.text)

def print_categorymembers(categorymembers, level=0, max_level=4, prev_cat=[]):
    for c in categorymembers.values():
        if c.ns == wikipediaapi.Namespace.MAIN:
            cat = prev_cat[-1] if prev_cat else "Root"
            if (page_count.get(cat , 0) == 5):
                continue
            page_count[cat] = page_count.get(cat, 0) + 1
            print("Visiting page: " + c.title)
            page_list.append((prev_cat, c.title))
            download_page_db(prev_cat, c.title)
            # Increment the value in the hashmap for the category
        if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
            cat = prev_cat[-1] if prev_cat else "Root"
            if (category_count.get(cat , 0) == 5):
                continue
            category_count[cat] = category_count.get(cat, 0) + 1
            print("Visiting category: " + c.title)
            new_cat = prev_cat + [c.title.replace("Category:", "")]
            print_categorymembers(c.categorymembers, level=level + 1, max_level=max_level, prev_cat=new_cat)




cursor = mydb.cursor()

cat = wiki_wiki.page("Category:Physics")
print_categorymembers(cat.categorymembers)




# Commit changes and close connection

mydb.close()

