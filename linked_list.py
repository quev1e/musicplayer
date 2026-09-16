

class LinkedListItem:
    """Узел связного списка"""
    def __init__(self, track):
        self.track = track
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

    def __eq__(self, other):
        """Сравнивает узел с другим узлом или его данными."""
        if isinstance(other, LinkedListItem):
            return self.track == other.track

        return self.track == other

    def __repr__(self):
        return f"LinkedListItem({self.track!r})"

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

        if self.first_item is None:
            raise ValueError("Элемент отсутствует в списке")

        current = self.first_item

        for _ in range(self._length):
            if current.track == item:
                prev_item = current.previous_item
                next_item = current.next_item

                prev_item.next_item = next_item
                next_item.previous_item = prev_item

                break
            current = current.next_item

        else:
            raise ValueError("Элемент отсутствует в списке")

        if self._length == 1:
            self._first_item = None
            self._length = 0
            return

        if current is self.first_item:
            self._first_item = next_item

        current.next_item = None
        current.previous_item = None

        self._length -= 1


    def insert(self, previous, item):
        """Вставка справа"""
        next_item = previous.next_item
        new_item = LinkedListItem(item)

        new_item.previous_item = previous
        new_item.next_item = next_item
        previous.next_item = new_item
        self._length += 1


    def __len__(self):
        "Количество узлов."
        return self._length

    def __iter__(self):
        """Итерация узлов от первого к последнему."""
        current = self.first_item

        for _ in range(self._length):
            yield current
            current = current.next_item

    def __getitem__(self, index):
        "Обращение к узлу по индексу."
        if not isinstance(index, int):
            raise TypeError("Индекс должен быть целым числом")
        if index < 0:
            index += self._length

        if index < 0 or index >= self._length:
            raise IndexError("Индекс находится вне границ списка")

        current = self.first_item
        for _ in range(index):
            current = current.next_item

        return current

    def __contains__(self, item):
        """Проверка наличия данных в списке."""
        for node in self:
            if node.track == item:
                return True

        return False

    def __reversed__(self):
        """Элементы списка в обратном порядке."""
        current = self.last

        for _ in range(self._length):
            yield current.track
            current = current.previous_item




