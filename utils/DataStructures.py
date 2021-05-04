# -*- coding: utf-8 -*-

class Queue(object):
    def __init__(self, size=10):
        self.queue = []
        self.max_size = size

    def __repr__(self):
        return f'Values: {self.queue}'

    def add(self, item):
        if len(self.queue) < self.max_size:
            self.queue.append(item)
        else:
            self.queue = self.queue[1:]
            self.queue.append(item)

    def get_items(self):
        return self.queue

    def pop_item(self):
        if len(self.queue) >= 1:
            self.queue.pop(0)
