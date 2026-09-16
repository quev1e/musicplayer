from linked_list import LinkedList, LinkedListItem
from audioplayer import AudioPlayer
from composition import Composition


class Playlist(LinkedList):

    def __init__(self, title: str, player: AudioPlayer):
        super().__init__()
        self.title = title
        self.player = player
        self._current_item = None # LinkedListItem


    def _contains_node(self, node):

        current_item = self.first_item

        for _ in range(self._length):

            if current_item is node:
                return True
            current_item = current_item.next_item

        return False

    @property
    def current(self):

        if self._current_item is None:
            return None

        return self._current_item

    def play_all(self, track: Composition):
        
        current_item = self.first_item
        
        for _ in range(self._length):
            if current_item.track is track:
                self._current_item = current_item
                self.player.play(track.filepath)
                return self.current

            current_item = current_item.next_item

        raise ValueError("Элемент отсутствует в списке")


    def next_track(self):

        if self._current_item is None:
            return None

        self._current_item = self._current_item.next_item
        song = self._current_item.track.filepath
        self.player.play(song)
        return self.current

    def previous_track(self):

        if self._current_item is None:
            return None

        self._current_item = self._current_item.previous_item
        song = self._current_item.track.filepath
        self.player.play(song)
        return self.current

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
