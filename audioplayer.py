from pathlib import Path
import pygame


MUSIC_END = pygame.USEREVENT + 1


class AudioPlayer:
    
    def  __init__(self):
        self._initialized = False
    
    def initialize(self):
        
        if not self._initialized:
            pygame.mixer.init()
            pygame.mixer.music.set_endevent(MUSIC_END)
            self._initialized = True
    
    def play(self, filepath):
        
        if not self._initialized:
            self.initialize()
        
        path = Path(filepath)
        
        if not path.is_file():
            raise FileNotFoundError("Файл не найден!")
        
        pygame.mixer.music.load(str(path))
        pygame.mixer.music.play()
    
    def pause(self):
        
        if self._initialized:
            pygame.mixer.music.pause()
    
    def stop(self):
        
        if self._initialized:
            pygame.mixer.music.stop()
            
    def resume(self):
        
        if self._initialized:
            pygame.mixer.music.unpause()
        
    def close(self):
        """Закрывает проигрыватель."""

        if self._initialized:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            self._initialized = False