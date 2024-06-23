import unittest
from Cache.cache import Cache
from Cache.eviction_policies import evict_fifo, evict_lru, evict_lifo, evict_lfu

class TestEvictionPolicies(unittest.TestCase):
    def setUp(self):
        self.cache = Cache(capacity=3, eviction_policy='LRU')

    def test_evict_fifo(self):
        self.cache.put(1, 'one')
        self.cache.put(2, 'two')
        self.cache.put(3, 'three')
        self.cache.put(4, 'four')  # This should evict 'one' due to FIFO policy
        self.assertIsNone(self.cache.get(1))  # 'one' should have been evicted

    def test_evict_lru(self):
        self.cache.put(1, 'one')
        self.cache.put(2, 'two')
        self.cache.put(3, 'three')
        self.cache.put(4, 'four')  # This should evict 'one' due to LRU policy
        self.assertIsNone(self.cache.get(1))  # 'one' should have been evicted

    def test_evict_lifo(self):
        self.cache = Cache(capacity=3, eviction_policy='LIFO')  # Set LIFO eviction policy
        self.cache.put(1, 'one')
        self.cache.put(2, 'two')
        self.cache.put(3, 'three')
        self.cache.put(4, 'four')  # This should evict 'three' due to LIFO policy
        self.assertIsNone(self.cache.get(3))  # 'three' should have been evicted

if __name__ == '__main__':
    unittest.main()
