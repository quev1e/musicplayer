

class Composition:
    
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
    