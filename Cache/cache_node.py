import time

class CacheNode:
    def __init__(self, key, value, ttl=None):
        self.key = key
        self.value = value
        self.ttl = ttl
        self.expiry_time = time.time() + ttl if ttl else None
        self.next = None
        self.prev = None
        self.frequency = 1 
        self.freq_node = None
