"""Модуль интерфейса музыкального плеера."""


import sys
import json

from pathlib import Path
from mutagen.id3 import ID3, ID3NoHeaderError
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QLineEdit,
    QGroupBox,
    QVBoxLayout,
    QHBoxLayout,
    QMainWindow,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QFileDialog
)

from audioplayer import AudioPlayer
from playlist import Playlist
from composition import Composition

class MusicPlayer(QMainWindow):
    """Окно музыкального плеера."""
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Player")
        self.resize(400, 600)

        # Главный layout
        self.main_layout = QHBoxLayout()
        self.main_layout.setSpacing(15)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        # Центральный widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(self.main_layout)

        self.data_file = Path("playlists.json")
        self.default_cover = (
            Path(__file__).parent
            / "assets"
            / "default_cover.png"
        )
        self.player = AudioPlayer()
        self.playlists = [] # хранит объекты Playlist

        self.selected_playlist = None
        self.selected_track = None
        self.current_playlist = None
        self.current_track = None

        self.is_playing = False
        self.is_paused = False

        # ТРИ ПАНЕЛИ
        self.create_playlists_panel()
        self.create_tracks_panel()
        self.create_current_track_panel()

        self.main_layout.setStretch(0, 1)
        self.main_layout.setStretch(1, 2)
        self.main_layout.setStretch(2, 1)

    def create_playlists_panel(self):
        """Создаёт левую панель плейлистов."""

        self.playlist_panel = QGroupBox()
        playlist_layout = QVBoxLayout()
        playlist_layout.setContentsMargins(
            15,
            4,
            15,
            15,
        )
        playlist_layout.setSpacing(15)

        playlists_panel_name = QLabel('Playlist')
        playlists_panel_name.setFixedHeight(24)
        playlists_panel_name.setAlignment(
            Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.playlist_list = QListWidget() # хранит str и объекты LinkedlistItem
        self.playlist_list.currentItemChanged.connect(
            self.on_playlist_selected
        )

        self.load_playlists() # загружает список плейлистов в self.playlists
        # отображает список плейтистов из self.playlists в self.playlist_list = QListWidget()
        self.refresh_playlist_list()

        self.new_playlist_name = QLineEdit()
        self.new_playlist_name.setPlaceholderText("Введите название плейлиста...")

        self.create_playlist_button = QPushButton("Create Playlist")
        self.create_playlist_button.clicked.connect(self.create_playlist)

        self.delete_playlist_button = QPushButton("Delete Playlist")
        self.delete_playlist_button.clicked.connect(self.delete_playlist)

        playlist_layout.addWidget(playlists_panel_name)
        playlist_layout.addWidget(self.playlist_list, 1)
        playlist_layout.addWidget(self.new_playlist_name)
        playlist_layout.addWidget(self.create_playlist_button)
        playlist_layout.addWidget(self.delete_playlist_button)

        self.playlist_panel.setLayout(playlist_layout)
        self.main_layout.addWidget(self.playlist_panel)

    def create_tracks_panel(self):
        "Создаёт среднюю панель треков."

        self.tracks_panel = QGroupBox()
        tracks_layout = QVBoxLayout()
        tracks_layout.setContentsMargins(
            15,
            4,
            15,
            15,
        )
        tracks_layout.setSpacing(15)

        tracks_panel_name = QLabel("Tracks")
        tracks_panel_name.setFixedHeight(24)
        tracks_panel_name.setAlignment(
            Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.track_list = QListWidget()
        self.track_list.currentItemChanged.connect(
            self.on_track_selected
        )
        self.track_list.itemDoubleClicked.connect(
            self.double_clicked
        )

        self.refresh_tracks()

        # Кнопки перемещения выбранного трека
        up_and_down_layout = QHBoxLayout()

        self.up_track_button = QPushButton("Up")
        self.up_track_button.clicked.connect(self.up_track)

        self.down_track_button = QPushButton("Down")
        self.down_track_button.clicked.connect(self.down_track)

        up_and_down_layout.addWidget(self.up_track_button)
        up_and_down_layout.addWidget(self.down_track_button)

        self.add_track_button = QPushButton("Add")
        self.add_track_button.clicked.connect(self.add_track)

        self.delete_track_button = QPushButton("Delete")
        self.delete_track_button.clicked.connect(self.delete_track)

        tracks_layout.addWidget(tracks_panel_name)
        tracks_layout.addWidget(self.track_list, 1)
        tracks_layout.addLayout(up_and_down_layout)
        tracks_layout.addWidget(self.add_track_button)
        tracks_layout.addWidget(self.delete_track_button)

        self.tracks_panel.setLayout(tracks_layout)
        self.main_layout.addWidget(self.tracks_panel)

    def create_current_track_panel(self):
        """Создаёт панель текущего трека."""

        self.current_track_panel = QGroupBox()
        current_track_layout = QVBoxLayout()
        current_track_layout.setContentsMargins(
            15,
            4,
            15,
            15,
        )
        current_track_layout.setSpacing(15)

        current_track_panel_name = QLabel("Now Playing")
        current_track_panel_name.setFixedHeight(24)
        current_track_panel_name.setAlignment(
            Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.cover_label = QLabel()
        self.cover_label.setFixedSize(350, 350)
        self.cover_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.filepath_label = QLabel()
        self.filepath_label.setObjectName(
            "songname"
        )

        cover_vlayout = QVBoxLayout()

        cover_hlayout = QHBoxLayout()
        cover_hlayout.addStretch()
        cover_hlayout.addWidget(self.cover_label)
        cover_hlayout.addStretch()

        cover_vlayout.addStretch()
        cover_vlayout.addLayout(cover_hlayout)
        cover_vlayout.addWidget(self.filepath_label)
        cover_vlayout.addStretch()

        buttons_layout = QHBoxLayout()

        self.prev_button = QPushButton("⏮️")
        self.prev_button.clicked.connect(self.on_prev_track)

        self.play_pause_button = QPushButton("▶️")
        self.play_pause_button.clicked.connect(self.play_or_pause)

        self.next_button = QPushButton("⏭️")
        self.next_button.clicked.connect(self.on_next_track)

        self.stop_button = QPushButton("⏹️")
        self.stop_button.clicked.connect(self.on_stop)

        self.prev_button.setObjectName(
            "currentTrackButton"
        )
        self.play_pause_button.setObjectName(
            "currentTrackButton"
        )
        self.next_button.setObjectName(
            "currentTrackButton"
        )
        self.stop_button.setObjectName(
            "currentTrackButton"
        )

        buttons_layout.addWidget(self.prev_button)
        buttons_layout.addWidget(self.play_pause_button)
        buttons_layout.addWidget(self.next_button)
        buttons_layout.addWidget(self.stop_button)

        current_track_layout.addWidget(current_track_panel_name)
        current_track_layout.addLayout(cover_vlayout)
        current_track_layout.addLayout(buttons_layout)

        self.current_track_panel.setLayout(current_track_layout)
        self.main_layout.addWidget(self.current_track_panel)

        self.clear_current_track()


    # СЛОТЫ ПЛЕЙЛИСТОВ
    # Загрузка и обновление
    def save_playlists(self):
        """Сохраняет изменения в списке плейлистов в JSON-файл."""

        data = [playlist.to_dict() for playlist in self.playlists]

        with self.data_file.open(
            "w", # перезаписываем файл с 0
            encoding="utf-8",
        ) as file:

            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=2,
            )

    def load_playlists(self):
        """Загружает объекты Playlist в self.playlists из JSON-файла."""

        if not self.data_file.exists():
            return

        try:
            with self.data_file.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

        except json.JSONDecodeError:
            QMessageBox.warning(
                self,
                "Ошибка файла",
                "Файл playlists.json повреждён.",
            )
            return

        if not isinstance(data, list):
            QMessageBox.warning(
                self,
                "Ошибка данных",
                "Корень JSON должен быть списком.",
            )
            return

        self.playlists.clear()

        for playlist_data in data:
            playlist = Playlist.from_dict(playlist_data, self.player)
            self.playlists.append(playlist)

    def refresh_playlist_list(self):
        """Отображает список плейлистов из self.playlists 
        в self.playlist_list = QListWidget()."""

        self.playlist_list.clear()

        for playlist in self.playlists:
            item = QListWidgetItem(playlist.title)
            item.setData(Qt.ItemDataRole.UserRole, playlist)
            self.playlist_list.addItem(item)

    # Обработка кнопок
    def on_playlist_selected(self, current, previous):
        """Обрабатывает выбор плейлиста."""

        if current is None:
            self.selected_playlist = None
            self.selected_track = None
            self.refresh_tracks()
            return

        self.selected_playlist = current.data(Qt.ItemDataRole.UserRole)
        self.selected_track = None

        self.track_list.blockSignals(True)

        try:
            self.refresh_tracks()
        finally:
            self.track_list.blockSignals(False)

    def create_playlist(self):
        """Создаёт плейлист с названием из self.new_playlist_name."""

        title = self.new_playlist_name.text().strip()

        if not title:
            QMessageBox.warning(
                self,
                "Пустое название",
                "Введите название плейлиста.",
            )
            return

        if any(
            playlist.title == title for playlist in self.playlists
        ):
            QMessageBox.warning(
                self,
                "Дубликат",
                "Такое название уже есть.",
            )
            return

        playlist = Playlist(title, self.player)
        self.playlists.append(playlist)

        self.save_playlists()
        self.refresh_playlist_list()
        self.new_playlist_name.clear()
        self.playlist_list.setCurrentRow(
            self.playlist_list.count() - 1
        )

    def delete_playlist(self):
        """Удаляет выбранный плейлист."""

        if not self.validate_selection(
            require_track=False
        ):
            return

        deleted_playlist = self.selected_playlist
        deleting_current_playlist = deleted_playlist is self.current_playlist

        self.playlists.remove(deleted_playlist)

        if deleting_current_playlist:
            self.player.stop()

            self.current_playlist = None
            self.current_track = None
            self.set_stopped_state()

        self.selected_playlist = None
        self.selected_track = None

        self.save_playlists()
        self.refresh_playlist_list()

        if not self.playlists:
            self.refresh_tracks()
            self.clear_current_track()
            return

        self.playlist_list.setCurrentRow(0)

    # СЛОТЫ ТРЕКОВ
    # Обновление
    def refresh_tracks(self):
        """Отображает список треков выбранного плейлиста."""

        self.track_list.clear()

        if self.selected_playlist is None:
            return

        for node in self.selected_playlist:
            path = Path(node.track.filepath).name[:-4]
            item = QListWidgetItem(path)
            item.setData(Qt.ItemDataRole.UserRole, node)
            self.track_list.addItem(item)

    # Валидатор
    def validate_selection(self, require_track=True, require_tracks_in_playlist=False):
        """Проверяет выбранные плейлист и трек."""

        if self.selected_playlist is None:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Выберите плейлист.",
            )
            return False

        if require_track and self.selected_track is None:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Выберите трек.",
            )
            return False

        if require_tracks_in_playlist and len(self.selected_playlist) == 0:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Плейлист пуст.",
            )
            return False

        return True

    # Вспомогательные функции
    def set_playing_state(self):
        """Устанавливает состояние воспроизведения."""

        self.is_playing = True
        self.is_paused = False
        self.play_pause_button.setText(
            "⏸️"
        )

    def set_paused_state(self):
        """Устанавливает состояние паузы."""

        self.is_playing = False
        self.is_paused = True
        self.play_pause_button.setText(
            "▶️"
        )

    def set_stopped_state(self):
        """Устанавливает остановленное состояние."""

        self.is_playing = False
        self.is_paused = False
        self.play_pause_button.setText(
            "▶️"
        )

    # Обработка кнопок
    def on_track_selected(self, current, previous):
        """Обрабатывает выбор трека."""

        if current is None:
            self.selected_track = None
            return

        self.selected_track = current.data(Qt.ItemDataRole.UserRole)

        if self.current_track:
            return

        composition = self.selected_track.track

        self.show_composition(composition)

    def move_track_up_or_down(self, direction):
        """Перемещает выбранный трек."""

        if not self.validate_selection():
            return

        current_row = self.track_list.currentRow()
        last_row = self.track_list.count() - 1

        if direction == "up":
            if current_row <= 0:
                return

            new_row = current_row - 1
            self.selected_playlist.move_up(
                self.selected_track
            )

        else:
            if current_row >= last_row:
                return

            new_row = current_row + 1
            self.selected_playlist.move_down(
                self.selected_track
            )

        self.save_playlists()

        self.track_list.blockSignals(True)

        try:
            self.refresh_tracks()
            self.track_list.setCurrentRow(new_row)
        finally:
            self.track_list.blockSignals(False)

        self.selected_track = (
            self.track_list.currentItem().data(
                Qt.ItemDataRole.UserRole
            )
        )

    def up_track(self):
        "Поднимает выбранный трек вверх в очереди на 1."
        self.move_track_up_or_down("up")

    def down_track(self):
        "Опускает выбранный трек вверх в очереди на 1."
        self.move_track_up_or_down("down")

    def add_track(self):
        "Добавляет  в плейлист трек с заданным filepath."

        if not self.validate_selection(require_track=False):
            return

        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите аудиофайл",
            "",
            "Audio Files (*.mp3 *.wav *.ogg);;All Files (*)",
        )

        if not filepath:
            return

        path = Path(filepath)

        for node in self.selected_playlist:
            if node.track.filepath == str(path):
                QMessageBox.warning(
                    self,
                    "Дубликат",
                    "Этот трек уже есть в плейлисте.",
                )
                return

        composition = Composition(filepath=str(path))

        self.selected_playlist.append(composition)
        self.save_playlists()
        self.refresh_tracks()
        self.track_list.setCurrentRow(
            self.track_list.count() - 1
        )

    def delete_track(self):
        "Удаляет выбранный трек из плейлиста."

        if not self.validate_selection():
            return

        self.selected_playlist.remove(self.selected_track)
        self.selected_track = None
        self.clear_current_track()
        self.save_playlists()
        self.refresh_tracks()

    # ТЕКУЩИЙ ТРЕК
    # Обработка обложки
    def show_default_cover(self):
        """Показывает обложку текущего трека по умолчанию."""

        pixmap = QPixmap(
            str(self.default_cover)
        )

        if pixmap.isNull():
            self.cover_label.clear()
            self.cover_label.setText("No cover")
            return

        pixmap = pixmap.scaled(
            self.cover_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.cover_label.setPixmap(pixmap)

    def get_embedded_cover(self, filepath):
        """Извлекает встроенную обложку трека из .mp3."""

        try:
            tags = ID3(filepath)
        except ID3NoHeaderError:
            return None

        for key in tags:
            if key.startswith("APIC"):
                return tags[key].data

        return None

    def show_cover(self, filepath):
        """Показывает встроенную обложку 
        трека или изображение по умолчанию."""

        cover_data = self.get_embedded_cover(
            filepath
        )

        if cover_data is None:
            self.show_default_cover()
            return

        pixmap = QPixmap()

        if not pixmap.loadFromData(cover_data):
            self.show_default_cover()
            return

        pixmap = pixmap.scaled(
            self.cover_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.cover_label.setPixmap(pixmap)

    # Обновление панели треков
    def show_composition(self, composition):
        """Отображение выбранного трека в правой панели."""
        filename = Path(
            composition.filepath
        ).name

        self.filepath_label.setText(
            f"{filename[:-4]}"
        )

        self.show_cover(composition.filepath)

    def clear_current_track(self):
        """Состояние правой панели если текущего трека нет."""

        if self.selected_track is not None:
            return

        self.player.stop()
        self.set_stopped_state()

        self.filepath_label.setText(
            "Choose a track . . ."
        )
        self.show_default_cover()

    # Слоты текущего трека
    def move_current_track(self, direction):
        """Переходит к соседнему треку."""

        if not self.validate_selection(require_tracks_in_playlist=True):
            return

        if self.selected_playlist.current is None:
            self.selected_playlist._current_item = (
                self.selected_playlist.first_item
            )

            self.selected_playlist.player.play(
                self.selected_playlist.current.track.filepath
            )
        elif direction == 'next':
            self.selected_playlist.next_track()
        else:
            self.selected_playlist.previous_track()

        self.selected_track = self.selected_playlist.current
        self.current_playlist = self.selected_playlist
        self.current_track = self.selected_track

        self.show_composition(self.selected_track.track)

        self.track_list.blockSignals(True)

        try:
            self.refresh_tracks()

            for row in range(self.track_list.count()):
                item = self.track_list.item(row)
                node = item.data(
                    Qt.ItemDataRole.UserRole
                )

                if node is self.selected_track:
                    self.track_list.setCurrentRow(row)
                    break

        finally:
            self.track_list.blockSignals(False)

        self.set_playing_state()

    def on_next_track(self):
        """Переходит к следующему треку."""
        self.move_current_track("next")

    def on_prev_track(self):
        """Переходит к предыдущему треку."""
        self.move_current_track("previous")

    def on_stop(self):
        """Останавливает воспроизведение трека."""

        self.player.stop()

        self.selected_track = None
        self.current_track = None
        self.current_playlist = None

        self.set_stopped_state()

        self.track_list.clearSelection()
        self.clear_current_track()

    def play_or_pause(self):
        """Ставит трек на паузу или снимает с паузы."""

        if not self.validate_selection():
            return

        if self.is_playing:
            self.player.pause()
            self.set_paused_state()
            return

        if self.is_paused:
            self.player.resume()
            self.set_playing_state()
            return

        self.selected_playlist.play_all(self.selected_track)
        self.current_playlist = self.selected_playlist
        self.current_track = self.selected_track
        self.set_playing_state()

    def double_clicked(self, item):
        """Обрабатывает случай двойного нажатия на трек в списке."""

        if not self.validate_selection(require_track=False):
            return

        clicked_item = item.data(Qt.ItemDataRole.UserRole)
        self.selected_track = clicked_item

        if self.current_track == clicked_item:
            self.play_or_pause()

        else:
            self.selected_playlist.play_all(clicked_item)
            self.current_playlist = self.selected_playlist
            self.current_track = clicked_item
            self.selected_track = clicked_item

            self.set_playing_state()

            self.show_composition(self.current_track.track)

    def closeEvent(self, event):
        """Закрывает плеер."""
        self.player.close()
        event.accept()

def load_stylesheet(app):
    """Загружает стили приложения."""

    style_path = (
        Path(__file__).parent / "style.qss"
    )

    app.setStyleSheet(
        style_path.read_text(
            encoding="utf-8"
        )
    )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    load_stylesheet(app)
    window = MusicPlayer()
    window.show()
    sys.exit(app.exec())
    