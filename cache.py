from collections import OrderedDict

class Cache:
    def __init__(self):
        self.capacity = 100
        self.cache = OrderedDict()

    def get(self, key):
        if key in self.cache:
            # Move the accessed key to the end to maintain order
            self.cache.move_to_end(key)
            return self.cache[key]
        else:
            return None
    
    def get_keys(self):
        return self.cache.keys()
    
    def get_by_content(self, content):
        matching_items = []
        for key, value in self.cache.items():
            if content in str(value["content"]):
                matching_items.append((key, value))
        return matching_items

    def put(self, key, value):
        if key in self.cache:
            # Move the existing key to the end to maintain order
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            # If capacity is reached, remove the first (oldest) item
            self.cache.popitem(last=False)
        self.cache[key] = value
