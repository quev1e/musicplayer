import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from pathlib import Path
import json

import pygame

from audioplayer import MUSIC_END, AudioPlayer
from composition import Composition
from playlist import Playlist


class MusicApp:
    """Простой интерфейс музыкального плеера."""

    def __init__(self, root):
        """Создаёт приложение."""

        self.root = root
        self.root.title("Музыкальный плеер")
        self.root.geometry("800x500")
        self.root.minsize(700, 400)

        pygame.init()
        pygame.display.set_mode((1, 1))
        
        self.is_paused = False
        self.stop_requested = False

        self.player = AudioPlayer()

        self.playlists = {}

        self.playlist = Playlist(
            "Моя музыка",
            self.player,
        )

        self.playlists["Моя музыка"] = self.playlist

        self.create_interface()
        self.load_playlists()

        self.root.after(100, self.check_music_events)

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close,
        )

    def create_interface(self):
        """Создаёт все элементы интерфейса."""
        
        icons_folder = Path(__file__).parent / "icons"

        self.icons = {
            "add": tk.PhotoImage(
                file=icons_folder / "add.png",
            ),
            "delete": tk.PhotoImage(
                file=icons_folder / "delete.png",
            ),
            "play": tk.PhotoImage(
                file=icons_folder / "play.png",
            ),
            "pause": tk.PhotoImage(
                file=icons_folder / "pause.png",
            ),
            "next": tk.PhotoImage(
                file=icons_folder / "next.png",
            ),
            "previous": tk.PhotoImage(
                file=icons_folder / "previous.png",
            ),
            "stop": tk.PhotoImage(
                file=icons_folder / "stop.png",
            ),
        }

        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(
            side=tk.LEFT,
            fill=tk.Y,
            padx=10,
            pady=10,
        )

        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=10,
        )

        playlists_label = tk.Label(
            self.left_frame,
            text="Плейлисты",
            font=("Arial", 12, "bold"),
        )
        playlists_label.pack(pady=(0, 5))

        self.playlists_box = tk.Listbox(
            self.left_frame,
            width=20,
            height=20,
        )
        self.playlists_box.pack(
            fill=tk.Y,
            expand=True,
        )

        self.playlists_box.insert(
            tk.END,
            self.playlist.title,
        )
        
        self.playlists_box.bind(
            "<<ListboxSelect>>",
            self.select_playlist,
        )
        
        playlist_buttons = tk.Frame(self.left_frame)
        playlist_buttons.pack(
            fill=tk.X,
            pady=(10, 0),
        )

        new_playlist_button = tk.Button(
            playlist_buttons,
            image=self.icons["add"],
            width=50,
            height=50,
            command=self.create_playlist,
        )
        
        new_playlist_button.pack(
            side=tk.LEFT,
            expand=True,
            fill=tk.X,
            padx=2,
        )

        delete_playlist_button = tk.Button(
            playlist_buttons,
            image=self.icons["delete"],
            width=50,
            height=50,
            command=self.delete_playlist,
        )
        delete_playlist_button.pack(
            side=tk.LEFT,
            expand=True,
            fill=tk.X,
            padx=2,
)

        tracks_label = tk.Label(
            self.right_frame,
            text="Композиции",
            font=("Arial", 12, "bold"),
        )
        tracks_label.pack(pady=(0, 5))

        self.buttons_frame = tk.Frame(self.right_frame)
        self.buttons_frame.pack(
            side=tk.BOTTOM,
            fill=tk.X,
            pady=(10, 0),
        )

        self.tracks_box = tk.Listbox(
            self.right_frame,
            width=60,
            height=18,
        )
        self.tracks_box.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True,
        )

        add_button = tk.Button(
            self.buttons_frame,
            image=self.icons["add"],
            width=50,
            height=50,
            command=self.add_track,
        )
        add_button.pack(
            side=tk.LEFT,
            padx=3,
        )

        remove_button = tk.Button(
            self.buttons_frame,
            image=self.icons["delete"],
            width=50,
            height=50,
            text="Удалить",
            command=self.remove_track,
        )
        remove_button.pack(
            side=tk.LEFT,
            padx=3,
        )

        play_button = tk.Button(
            self.buttons_frame,
            image=self.icons["play"],
            width=50,
            height=50,
            command=self.play_selected,
        )
        play_button.pack(
            side=tk.LEFT,
            padx=3,
        )
        
        previous_button = tk.Button(
            self.buttons_frame,
            image=self.icons["previous"],
            width=50,
            height=50,
            command=self.previous_track,
        )
        previous_button.pack(
            side=tk.LEFT,
            padx=3,
        )
        
        
        pause_button = tk.Button(
            self.buttons_frame,
            image=self.icons["pause"],
            width=50,
            height=50,
            command=self.pause_or_resume,
        )
        pause_button.pack(
            side=tk.LEFT,
            padx=3,
)

        next_button = tk.Button(
            self.buttons_frame,
            image=self.icons["next"],
            width=50,
            height=50,
            command=self.next_track,
        )
        next_button.pack(
            side=tk.LEFT,
            padx=3,
        )

        stop_button = tk.Button(
            self.buttons_frame,
            image=self.icons["stop"],
            width=50,
            height=50,
            command=self.stop,
        )
        stop_button.pack(
            side=tk.LEFT,
            padx=3,
        )

    def get_save_path(self):
        """Возвращает путь к файлу сохранения."""
        return Path(__file__).parent / "playlist.json"

    def save_playlists(self):
        """Сохраняет все плейлисты в JSON-файл."""

        data = {}

        for name, playlist in self.playlists.items():
            data[name] = []

            for item in playlist:
                data[name].append(
                    {
                        "filepath": item.track.filepath,
                        "title": item.track.title,
                        "artist": item.track.artist,
                    }
                )

        with self.get_save_path().open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4,
            )
    
    def load_playlists(self):
        """Загружает все плейлисты из JSON-файла."""

        save_path = self.get_save_path()

        if not save_path.exists():
            self.refresh_tracks()
            return

        with save_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        self.playlists.clear()

        for name, tracks in data.items():
            playlist = Playlist(
                name,
                self.player,
            )

            for track_data in tracks:
                filepath = Path(track_data["filepath"])

                if not filepath.is_file():
                    continue

                song = Composition(
                    filepath=str(filepath),
                    title=track_data["title"],
                    artist=track_data["artist"],
                )

                playlist.append(song)

            self.playlists[name] = playlist

        if not self.playlists:
            self.playlist = Playlist(
                "Моя музыка",
                self.player,
            )
            self.playlists["Моя музыка"] = self.playlist
        else:
            first_name = next(iter(self.playlists))
            self.playlist = self.playlists[first_name]

        self.playlists_box.delete(
            0,
            tk.END,
        )

        for name in self.playlists:
            self.playlists_box.insert(
                tk.END,
                name,
            )

        self.playlists_box.selection_set(0)
        self.refresh_tracks()
    
    def create_playlist(self):
        """Создаёт новый плейлист."""

        name = simpledialog.askstring(
            "Новый плейлист",
            "Введите название плейлиста:",
            parent=self.root,
        )

        if name is None:
            return

        name = name.strip()

        if not name:
            messagebox.showwarning(
                "Ошибка",
                "Название не может быть пустым.",
            )
            return

        if name in self.playlists:
            messagebox.showwarning(
                "Ошибка",
                "Плейлист с таким названием уже существует.",
            )
            return

        new_playlist = Playlist(
            name,
            self.player,
        )

        self.playlists[name] = new_playlist

        self.playlists_box.insert(
            tk.END,
            name,
        )

        last_index = self.playlists_box.size() - 1

        self.playlists_box.selection_clear(
            0,
            tk.END,
        )
        self.playlists_box.selection_set(last_index)

        self.playlist = new_playlist
        self.refresh_tracks()
        self.save_playlists()
    
    
    def select_playlist(self, event=None):
        """Переключает текущий плейлист."""

        selected = self.playlists_box.curselection()

        if not selected:
            return

        index = selected[0]
        name = self.playlists_box.get(index)

        self.playlist = self.playlists[name]
        self.refresh_tracks()
    
    def delete_playlist(self):
        """Удаляет выбранный плейлист."""

        selected = self.playlists_box.curselection()

        if not selected:
            messagebox.showwarning(
                "Предупреждение",
                "Сначала выберите плейлист.",
            )
            return

        index = selected[0]
        name = self.playlists_box.get(index)

        if len(self.playlists) == 1:
            messagebox.showwarning(
                "Предупреждение",
                "Нельзя удалить последний плейлист.",
            )
            return

        answer = messagebox.askyesno(
            "Удаление",
            f"Удалить плейлист «{name}»?",
        )

        if not answer:
            return

        if self.playlist is self.playlists[name]:
            self.player.stop()

        del self.playlists[name]

        self.playlists_box.delete(index)

        self.playlists_box.selection_set(0)

        first_name = self.playlists_box.get(0)
        self.playlist = self.playlists[first_name]

        self.refresh_tracks()
        self.save_playlists()


    def add_track(self):
        """Добавляет аудиофайл через диалоговое окно."""

        filepath = filedialog.askopenfilename(
            title="Выберите аудиофайл",
            filetypes=[
                ("Audio files", "*.mp3 *.wav *.ogg"),
                ("All files", "*.*"),
            ],
        )

        if not filepath:
            return

        path = Path(filepath)

        song = Composition(
            filepath=str(path),
            title=path.stem,
            artist="Неизвестный исполнитель",
        )

        self.playlist.append(song)
        self.save_playlists()
        self.refresh_tracks()

    def remove_track(self):
        """Удаляет выбранный трек."""

        selected = self.tracks_box.curselection()

        if not selected:
            messagebox.showwarning(
                "Предупреждение",
                "Сначала выберите трек.",
            )
            return

        index = selected[0]
        item = self.playlist[index]

        if item is self.playlist.current:
            self.player.stop()
            self.stop_requested = True
            self.is_paused = False
            self.playlist.clear_current()

        self.playlist.remove(item)
        self.save_playlists()
        self.refresh_tracks()

    def play_selected(self):
        """Воспроизводит выбранный трек."""

        selected = self.tracks_box.curselection()

        if not selected:
            messagebox.showwarning(
                "Предупреждение",
                "Сначала выберите трек.",
            )
            return

        index = selected[0]
        item = self.playlist[index]

        self.stop_requested = False
        self.is_paused = False

        self.playlist.play_all(item.track)
        self.select_current_track()
    
    def pause_or_resume(self):
        """Ставит музыку на паузу или продолжает её."""

        if self.playlist.current is None:
            return

        if self.is_paused:
            self.player.resume()
            self.is_paused = False
        else:
            self.player.pause()
            self.is_paused = True

    def next_track(self):
        """Переходит к следующему треку."""

        if self.stop_requested:
            return

        if self.playlist.current is None:
            return

        self.playlist.next_track()
        self.is_paused = False
        self.select_current_track()
    
    def previous_track(self):
            """Переходит к предыдущему треку."""
    
            if self.stop_requested:
                return
    
            if self.playlist.current is None:
                return
    
            self.playlist.previous_track()
            self.is_paused = False
            self.select_current_track()

    def stop(self):
        """Останавливает музыку без запуска следующего трека."""

        self.stop_requested = True
        self.is_paused = False
        self.player.stop()

    def refresh_tracks(self):
        """Обновляет список треков на экране."""

        self.tracks_box.delete(
            0,
            tk.END,
        )

        for item in self.playlist:
            self.tracks_box.insert(
                tk.END,
                str(item.track),
            )

    def select_current_track(self):
        """Выделяет текущий трек."""

        current_item = self.playlist.current

        if current_item is None:
            return

        for index, item in enumerate(self.playlist):
            if item is current_item:
                self.tracks_box.selection_clear(
                    0,
                    tk.END,
                )
                self.tracks_box.selection_set(index)
                self.tracks_box.see(index)
                break

    def check_music_events(self):
        """Проверяет окончание текущего трека."""

        for event in pygame.event.get():
            if event.type == MUSIC_END:
                if not self.stop_requested:
                    self.next_track()

        self.root.after(
            100,
            self.check_music_events,
        )

    def close(self):
        """Сохраняет данные и закрывает приложение."""

        self.save_playlists()
        self.player.close()
        pygame.quit()
        self.root.destroy()



root = tk.Tk()
app = MusicApp(root)
root.mainloop()