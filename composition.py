"""Модуль музыкальной композиции."""


class Composition:
    """Класс музыкальной композиции."""

    def __init__(
        self,
        filepath: str,
        title=None,
        artist=None,
        album=None,
    ):

        self.title = title
        self.artist = artist
        self.album = album
        self.filepath = filepath

    @classmethod
    def from_dict(cls, data):
        """Преобразует данные JSON в объект класса."""
        return cls(
            filepath=data["filepath"],
            title=data.get("title"),
            artist=data.get("artist"),
            album=data.get("album"),
        )

    def to_dict(self):
        """Возвращает значения для хранения в JSON."""
        return {
            "filepath": self.filepath,
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
        }

    def __str__(self):
        """Возвращает название композиции."""
        return self.title

    def __repr__(self) -> str:
        """Возвращает техническое представление композиции."""
        return (
            f"Composition("
            f"title={self.title!r}, "
            f"artist={self.artist!r}, "
            f"filepath={self.filepath!r})"
        )
