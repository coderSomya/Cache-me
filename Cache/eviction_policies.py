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
