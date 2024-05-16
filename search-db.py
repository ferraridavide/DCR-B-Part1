import mysql.connector

from cache import Cache
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="my-secret-pw",
  database="dcr"
)

cursor = mydb.cursor(dictionary=True)

cache = Cache()

directory_id = 1

while True:
  pattern = input("\n\nInserisci termine ricerca: ")
  cache_hit = cache.get_by_content(pattern)
  cache_hit_keys = []

  if cache_hit is not None:
    cache_hit_keys = [key for key, value in cache_hit]
    for key, value in cache_hit:
      print("CACHE HIT: " + value["name"])

  except_ids = ','.join(str(str_keys) for str_keys in cache_hit_keys) if cache_hit_keys else ''
  cursor.callproc('Search', [directory_id, pattern, except_ids])

  from_db = 0
  for data in cursor.stored_results():
      for result in data.fetchall():
        from_db += 1
        cache.put(result["id"], result)
        print("FROM DB: " + result["name"])


  # Print percentage of cache hits and misses
  print(f"Cache hits: {len(cache_hit)}")
  print (f"Cache hit ratio: {len(cache_hit) / (len(cache_hit) + from_db) * 100:.2f}%")


mydb.close()