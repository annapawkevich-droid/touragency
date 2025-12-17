class InMemoryBookingRepo:

    def __init__(self):
        self._items = []

    def save(self, booking):
        self._items.append(booking)

    def list_all(self):
        return list(self._items)
     #тобто сама програма під час викоання зберігає в своїй програмі введені дані 
