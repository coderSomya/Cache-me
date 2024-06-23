def evict_fifo(cache):
    first = cache.head.next
    cache._remove(first)
    del cache.cache[first.key]
    cache.size -= 1

def evict_lru(cache):
    evict_fifo(cache)

def evict_lifo(cache):
    node = cache.stack.pop()
    cache._remove(node)
    del cache.cache[node.key]
    cache.size -= 1

#functions for LFU

class FrequencyNode:
    def __init__(self, frequency):
        self.frequency = frequency
        self.items = {}  # Maps key to CacheNode
        self.prev = None
        self.next = None

def evict_lfu(cache):
    if not cache.min_frequency_node:
        return
    min_freq_items = cache.min_frequency_node.items
    key_to_remove = next(iter(min_freq_items))
    node_to_remove = min_freq_items.pop(key_to_remove)
    cache._remove(node_to_remove)
    del cache.cache[key_to_remove]
    if not min_freq_items:
        cache._remove_frequency_node(cache.min_frequency_node)
    cache.size -= 1

def increment_frequency(cache, node):
    freq_node = node.freq_node
    if node.key in freq_node.items:
        del freq_node.items[node.key]
        if not freq_node.items:
            cache._remove_frequency_node(freq_node)
    node.frequency += 1
    if node.frequency not in cache.frequency_map:
        new_freq_node = FrequencyNode(node.frequency)
        add_frequency_node(cache, new_freq_node)
        cache.frequency_map[node.frequency] = new_freq_node
    cache.frequency_map[node.frequency].items[node.key] = node
    node.freq_node = cache.frequency_map[node.frequency]

def add_frequency_node(cache, node):
    cache.frequency_map[node.frequency] = node
    if not cache.min_frequency_node or node.frequency < cache.min_frequency_node.frequency:
        node.next = cache.min_frequency_node
        if cache.min_frequency_node:
            cache.min_frequency_node.prev = node
        cache.min_frequency_node = node
    else:
        current = cache.min_frequency_node
        while current.next and current.next.frequency < node.frequency:
            current = current.next
        node.next = current.next
        if current.next:
            current.next.prev = node
        current.next = node
        node.prev = current
        
def remove_frequency_node(cache, node):
    del cache.frequency_map[node.frequency]
    if node.prev:
        node.prev.next = node.next
    if node.next:
        node.next.prev = node.prev
    if cache.min_frequency_node == node:
        cache.min_frequency_node = node.next if node.next.frequency == node.frequency else None
