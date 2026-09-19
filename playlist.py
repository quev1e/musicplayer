"""Плейлисты на основе кольцевого двусвязного списка."""

from linked_list import LinkedList, LinkedListItem
from audioplayer import AudioPlayer
from composition import Composition


class Playlist(LinkedList):
    """Управление списком треков и его воспроизведением."""

    def __init__(self, title: str, player: AudioPlayer):
        super().__init__()
        self.title = title
        self.player = player
        self._current_item = None # LinkedListItem


    def _contains_node(self, node):
        """Проверяет наличие узла в списке."""

        current_item = self.first_item

        for _ in range(self._length):

            if current_item is node:
                return True
            current_item = current_item.next_item

        return False

    @property
    def current(self):
        """Возвращает текущий узел."""

        if self._current_item is None:
            return None

        return self._current_item

    def play_all(self, item: LinkedListItem):
        """Запускает выбранный трек и делает его текущим."""

        if not self._contains_node(item):
            raise ValueError(
                "Элемент отсутствует в списке"
            )

        self._current_item = item

        self.player.play(
            item.track.filepath
        )

        return self.current

    def next_track(self):
        """Запускает следующий трек."""

        if self._current_item is None:
            return None

        self._current_item = self._current_item.next_item
        song = self._current_item.track.filepath
        self.player.play(song)
        return self.current

    def previous_track(self):
        """Запускает предыдущий трек."""

        if self._current_item is None:
            return None

        self._current_item = self._current_item.previous_item
        song = self._current_item.track.filepath
        self.player.play(song)
        return self.current

    def move_down(self, item):
        """Перемещает трек на одну позицию вниз."""

        track = item.track

        if not self._contains_node(item):
            raise ValueError("Элемент отсутствует в списке")

        if self._length > 1:
            next_track = item.next_item.track
            item.next_item.track = track
            item.track = next_track

    def move_up(self, item):
        """Перемещает трек на одну позицию вверх."""

        track = item.track

        if not self._contains_node(item):
            raise ValueError("Элемент отсутствует в списке")

        if self._length > 1:
            prev_track = item.previous_item.track
            item.previous_item.track = track
            item.track = prev_track

    def clear_current(self):
        """Сбрасывает текущую композицию."""

        self._current_item = None

    def remove(self, item):
        """Удаляет узел из плейлиста."""

        if not self._contains_node(item):
            raise ValueError(
                "Элемент отсутствует в списке"
            )

        if item is self._current_item:
            self._current_item = None

        super().remove(item)

    @classmethod
    def from_dict(cls, data, player):
        """Преобразует данные из JSON в объект класса."""

        playlist = cls(data["title"], player)
        for track_data in data.get("tracks", []):
            composition = Composition.from_dict(track_data)
            playlist.append(composition)
        return playlist

    def to_dict(self):
        """Возвращает значения для хранения в JSON."""
        return {
            "title": self.title,
            "tracks": [
                node.track.to_dict()
                for node in self
            ]
        }
