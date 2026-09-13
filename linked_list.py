

class LinkedListItem:
    """Узел связного списка"""
    def __init__(self, data=None):
        self.data = data
        self._next = None
        self._previous = None

    @property
    def next_item(self):
        """Следующий элемент"""
        return self._next

    @next_item.setter
    def next_item(self, value):
        self._next = value

        if value is not None:
            value._previous = self

    @property
    def previous_item(self):
        """Предыдущий элемент"""
        return self._previous

    @previous_item.setter
    def previous_item(self, value):
        self._previous = value

        if value is not None:
            value._next = self

    def __repr__(self):
        return f'Item №{self.data}, previous: {self._previous}, next: {self._next}'

class LinkedList:
    """Связный список"""
    def __init__(self, first_item=None):
        self._first_item = first_item

        if first_item is None:
            self._length = 0
        else:
            self._length = self._calculate_length(first_item)

    @property
    def first_item(self):
        """Первый элемент"""
        return self._first_item

    @property
    def last(self):
        """Последний элемент"""
        if self._first_item is None:
            return None
        return self._first_item.previous_item
    
    @staticmethod
    def _calculate_length(first_item):
        length = 1
        current = first_item

        while current.next_item is not first_item:
            current = current.next_item
            length += 1

        return length


    def append_left(self, item):
        """Добавление слева"""

        new_item = LinkedListItem(item)

        if self.first_item is None:
            self._first_item = new_item
            new_item.previous_item = new_item
            new_item.next_item = new_item

        else:
            first_item = self.first_item
            last_item = self.last

            new_item.next_item = first_item
            new_item.previous_item = last_item

            first_item.previous_item = new_item
            last_item.next_item = new_item

            self._first_item = new_item

        self._length += 1

    def append_right(self, item):
        """Добавление справа"""
        new_item = LinkedListItem(item)

        if self.first_item is None:
            self._first_item = new_item
            new_item.previous_item = new_item
            new_item.next_item = new_item

        else:
            first_item = self.first_item
            last_item = self.last

            new_item.previous_item = last_item
            new_item.next_item = first_item
            last_item.next_item = new_item
            first_item.previous_item = new_item

        self._length += 1


    def append(self, item):
        self.append_right(item)

    def remove(self, item):
        """Удаление"""
        raise NotImplementedError()

    def insert(self, previous, item):
        """Вставка справа"""
        raise NotImplementedError()

    def __len__(self):
        raise NotImplementedError()

    def __iter__(self):
        raise NotImplementedError()

    def __getitem__(self, index):
        raise NotImplementedError()

    def __contains__(self, item):
        raise NotImplementedError()

    def __reversed__(self):
        raise NotImplementedError()
