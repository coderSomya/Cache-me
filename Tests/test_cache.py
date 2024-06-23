import unittest
from Cache.cache import Cache

class TestCache(unittest.TestCase):
    def setUp(self):
        self.cache = Cache(capacity=3, eviction_policy='LRU')  

    def test_put_get(self):
        self.cache.put(1, 'one')
        self.assertEqual(self.cache.get(1), 'one')

    def test_eviction(self):
        self.cache.put(1, 'one')
        self.cache.put(2, 'two')
        self.cache.put(3, 'three')
        self.cache.put(4, 'four')  # This should evict 'one' due to LRU policy
        self.assertIsNone(self.cache.get(1))  # 'one' should have been evicted

    def test_capacity(self):
        self.cache.put(1, 'one')
        self.cache.put(2, 'two')
        self.cache.put(3, 'three')
        self.cache.put(4, 'four')  # This should evict 'one'
        self.assertEqual(self.cache.size, 3)  # Cache size should remain 3

if __name__ == '__main__':
    unittest.main()