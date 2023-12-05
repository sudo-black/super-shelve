import shelve


class SuperShelve(shelve.Shelf):
    def __init__(self, filename, writeback_threshold=3000, **kwargs):
        super().__init__(filename, **kwargs)
        self._writeback_threshold = writeback_threshold
        self._operation_count = 0


    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._increment_operation()


    def __delitem__(self, key):
        super().__delitem__(key)
        self._increment_operation()


    def _increment_operation(self):
        self._operation_count += 1
        if self._operation_count >= self._writeback_threshold:
            self.sync()
            self._operation_count = 0


    def sync(self):
        if self.writeback:
            self._writeback()
        super().sync()
