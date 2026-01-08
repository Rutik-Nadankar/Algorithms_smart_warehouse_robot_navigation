import random

class Warehouse:
    def __init__(self, rows, cols, shelf_count=25):
        self.rows = rows
        self.cols = cols
        self.shelves = set()

        # Make sure shelves don't overlap and are within the grid
        while len(self.shelves) < shelf_count:
            r, c = random.randint(0, rows-1), random.randint(0, cols-1)
            self.shelves.add((r,c))

    def is_free(self, r, c):
        # Check boundaries and shelf locations
        return 0 <= r < self.rows and 0 <= c < self.cols and (r,c) not in self.shelves
