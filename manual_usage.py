from Cache import Cache

def eviction_callback():
    print("Item evicted from cache")

def hit_callback(key):
    print(f"Cache hit for key: {key}")

def miss_callback(key):
    print(f"Cache miss for key: {key}")


cache = Cache(2, eviction_policy='LRU')
cache.callbacks.on_eviction(eviction_callback)
cache.callbacks.on_hit(hit_callback)
cache.callbacks.on_miss(miss_callback)


cache.put(1, 'one')
cache.put(2, 'two')
print(cache.get(1))  # Cache hit
cache.put(3, 'three')  # Eviction happens
print(cache.get(2))  # Cache miss


