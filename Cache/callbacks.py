class Callbacks:
    def __init__(self):
        self.eviction_callbacks = []
        self.hit_callbacks = []
        self.miss_callbacks = []

    def on_eviction(self, callback):
        self.eviction_callbacks.append(callback)

    def on_hit(self, callback):
        self.hit_callbacks.append(callback)

    def on_miss(self, callback):
        self.miss_callbacks.append(callback)

    def execute_eviction_callbacks(self):
        for callback in self.eviction_callbacks:
            callback()

    def execute_hit_callbacks(self, key):
        for callback in self.hit_callbacks:
            callback(key)

    def execute_miss_callbacks(self, key):
        for callback in self.miss_callbacks:
            callback(key)
