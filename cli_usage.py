from Cache import Cache

print("Welcome to the In-Memory Cache System")

eviction_policy = input("Enter eviction policy (FIFO, LRU, LIFO): ").strip().upper()
capacity = int(input("Enter cache capacity: "))

cache = Cache(capacity, eviction_policy)

def eviction_callback():
    print("Item evicted from cache")

def hit_callback(key):
    print(f"Cache hit for key: {key}")

def miss_callback(key):
    print(f"Cache miss for key: {key}")

cache.callbacks.on_eviction(eviction_callback)
cache.callbacks.on_hit(hit_callback)
cache.callbacks.on_miss(miss_callback)

while True:
    command = input("Enter command (set/get/quit/display): ").strip().lower()

    if command == "set":
        key = input("Enter key: ")
        value = input("Enter value: ")
        ttl = input("Enter TTL (optional, press enter to skip): ").strip()
        ttl = int(ttl) if ttl else None
        cache.put(key, value, ttl)
        print(f"Set {key} = {value}")

    elif command == "get":
        key = input("Enter key: ")
        value = cache.get(key)
        if value is not None:
            print(f"Get {key} = {value}")
        else:
            print(f"{key} not found in cache")

    elif command == "display":
        print("Current cache state:")
        print(cache.display_cache())

    elif command == "quit":
        print("Exiting...")
        break

    else:
        print("Invalid command. Please enter 'set', 'get', 'quit', or 'display'.")


