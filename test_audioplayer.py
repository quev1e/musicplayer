import time
import pygame

from audioplayer import MUSIC_END, AudioPlayer
from composition import Composition
from playlist import Playlist


pygame.init()
pygame.display.set_mode((1, 1))

player = AudioPlayer()

song1 = Composition(
    filepath="music/Epica - Veniality.mp3",
    title="Veniality",
    artist="Epica",
)

song2 = Composition(
    filepath="music/Nightwish - Dark Chest of Wonders.mp3",
    title="Dark Chest of Wonders",
    artist="Nightwish",
)

playlist1 = Playlist("Эпика", player)
playlist1.append(song1)
playlist1.append(song2)

try:
    playlist1.play_all(song1)

    while True:
        for event in pygame.event.get():
            if event.type == MUSIC_END:
                print("Трек закончился")
                print("Следующий:", playlist1.next_track())

            if event.type == pygame.QUIT:
                raise KeyboardInterrupt

        time.sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    player.close()
    pygame.quit()
