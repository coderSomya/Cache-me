import threading
import time
import pickle
import json
from .cache_node import CacheNode
from .eviction_policies import evict_fifo, evict_lru, evict_lifo, evict_lfu, increment_frequency, add_frequency_node, remove_frequency_node, FrequencyNode
from .custom_exceptions import EvictionPolicyNotSupported
from .callbacks import Callbacks

class Cache:
    def __init__(self, capacity, eviction_policy='LRU'):
        self.capacity = capacity
        self.cache = {}
        self.size = 0
        self.lock = threading.Lock()
        self.callbacks = Callbacks()

        # Frequency map and minimum frequency node for LFU
        self.frequency_map = {}
        self.min_frequency_node = None

        # For LRU and FIFO
        self.head = CacheNode(None, None)  
        self.tail = CacheNode(None, None)  
        self.head.next = self.tail
        self.tail.prev = self.head

        # For LIFO
        self.stack = []

        # Initialize eviction policy
        self.eviction_policy = eviction_policy

    def get(self, key):
        with self.lock:
            if key in self.cache:
                node = self.cache[key]
                if node.expiry_time and node.expiry_time < time.time():
                    self._remove(node)
                    del self.cache[key]
                    self.size -= 1
                    self.callbacks.execute_miss_callbacks(key)
                    return None
                if self.eviction_policy == 'LRU':
                    self._remove(node)
                    self._add(node)
                elif self.eviction_policy == 'LFU':
                    increment_frequency(self, node)
                self.callbacks.execute_hit_callbacks(key)
                return node.value
            self.callbacks.execute_miss_callbacks(key)
            return None

    def put(self, key, value, ttl=None):
        with self.lock:
            if key in self.cache:
                node = self.cache[key]
                self._remove(node)
                node.value = value
                node.ttl = ttl
                node.expiry_time = time.time() + ttl if ttl else None
                if self.eviction_policy == 'LFU':
                    increment_frequency(self, node)
                else:
                    self._add(node)
            else:
                if self.size == self.capacity:
                    self._evict()
                new_node = CacheNode(key, value, ttl)
                self.cache[key] = new_node
                self._add(new_node)
                if self.eviction_policy == 'LFU':
                    if 1 not in self.frequency_map:
                        new_freq_node = FrequencyNode(1)
                        add_frequency_node(self, new_freq_node)
                        self.frequency_map[1] = new_freq_node
                    self.frequency_map[1].items[key] = new_node
                    new_node.freq_node = self.frequency_map[1]
                self.size += 1

    def _remove(self, node):
        if self.eviction_policy in ['FIFO', 'LRU']:
            if node.prev:
                node.prev.next = node.next
            if node.next:
                node.next.prev = node.prev
        elif self.eviction_policy == 'LFU':
            freq_node = node.freq_node
            if freq_node and node.key in freq_node.items:
                del freq_node.items[node.key]
                if not freq_node.items:
                    self._remove_frequency_node(freq_node)
            if node.prev:
                node.prev.next = node.next
            if node.next:
                node.next.prev = node.prev

    def _add(self, node):
        if self.eviction_policy in ['FIFO', 'LRU']:
            last = self.tail.prev
            last.next = node
            node.prev = last
            node.next = self.tail
            self.tail.prev = node
        elif self.eviction_policy == 'LFU':
            if 1 not in self.frequency_map:
                new_freq_node = FrequencyNode(1)
                add_frequency_node(self, new_freq_node)
                self.frequency_map[1] = new_freq_node
            freq_node = self.frequency_map[1]
            freq_node.items[node.key] = node
            node.freq_node = freq_node

    def _remove_frequency_node(self, freq_node):
        del self.frequency_map[freq_node.frequency]
        if freq_node.prev:
            freq_node.prev.next = freq_node.next
        if freq_node.next:
            freq_node.next.prev = freq_node.prev
        if self.min_frequency_node == freq_node:
            self.min_frequency_node = freq_node.next

    def _evict(self):
        eviction_methods = {
            'FIFO': evict_fifo,
            'LRU': evict_lru,
            'LIFO': evict_lifo,
            'LFU': evict_lfu,
        }
        if self.eviction_policy not in eviction_methods:
            raise EvictionPolicyNotSupported(f"Unsupported eviction policy: {self.eviction_policy}")

        eviction_methods[self.eviction_policy](self)
        self.callbacks.execute_eviction_callbacks()

    def save_to_file(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.cache, f)

    def load_from_file(self, filename):
        with open(filename, 'rb') as f:
            self.cache = pickle.load(f)
            self.size = len(self.cache)

    def to_json(self):
        return json.dumps({key: {'value': node.value, 'ttl': node.ttl} for key, node in self.cache.items()})

    def from_json(self, json_str):
        data = json.loads(json_str)
        for key, value in data.items():
            self.put(key, value['value'], ttl=value['ttl'])

    def get_stats(self):
        return {
            'hits': self.hits,
            'misses': self.misses,
            'evictions': self.evictions,
            'size': self.size,
            'capacity': self.capacity
        }

    def display_cache(self):
        with self.lock:
            if self.eviction_policy == 'LFU':
                freq_node = self.min_frequency_node
                cache_state = []
                while freq_node:
                    for key, node in freq_node.items.items():
                        cache_state.append(f"{key}: {node.value} (Freq: {node.frequency})")
                    freq_node = freq_node.next
                return " -> ".join(cache_state)
            else:
                current = self.head.next
                cache_state = []
                while current != self.tail:
                    cache_state.append(f"{current.key}: {current.value}")
                    current = current.next
                return " -> ".join(cache_state)

    def add_custom_eviction_policy(self, policy_name, policy_function):
        setattr(self, f"_evict_{policy_name.lower()}", policy_function)