# Database schema

**Data Consistency:**
- Foreign Key Rules: Ensures referential integrity between directories and files.
- On Delete Cascade: Automatically deletes all files and subdirectories when a directory is deleted, maintaining data consistency.
- Simplified renaming process since only the directory name needs to be updated, not the path of each file.
- Stores only the parent directory ID instead of the full path for each file, saving space.


The full database DDL can be found in 'ddl.sql'

# File Insert
 - Bulk Insertion: The files are inserted into the database in bulk using cursor.executemany, which improves performance compared to inserting each file individually.
 - Searchable Files: The script identifies and reads the content of specific file types (.txt, .html, .md) to store their content in the database.
 - Directory Hierarchy: The script maintains the directory hierarchy by tracking parent-child relationships and storing them in the database.


# Search with Stored Procedure and cache
 - Database Connection: Establishes a connection to the MySQL database.
 - Caching Mechanism: Utilizes a cache to store and retrieve search results to improve performance.
 - Search Operation: Executes a stored procedure to search for files in the database.
 - Cache Hit/Miss Calculation: Calculates and displays the percentage of cache hits and misses.
