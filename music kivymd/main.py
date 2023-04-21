import os
import time
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.button import MDIconButton
from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from mutagen.easyid3 import EasyID3
from kivy.uix.scrollview import ScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.list import OneLineListItem
from kivy.uix.slider import Slider
from kivy.uix.image import Image
import random

Window.size = (450, 700)


class MyApp(MDApp):

    def build(self):

        self.window_manager = ScreenManager(size=(450, 700))
        self.i = 0

        self.music_dir = "music_directory"

        self.music_files = os.listdir(self.music_dir)

        self.song_list = [x for x in self.music_files if x.endswith('mp3')]

        self.Main_window = Screen(size=(450, 700), name='main')

        self.my_layout = MDRelativeLayout(md_bg_color=[0, 0, 0, 0.8])

        self.list_for_playlist = []

        self.playlist = MDGridLayout(cols=1, spacing=5, size_hint_y=None, md_bg_color=[255, 255, 255, 0.4],
                                     size=(100, 200))
        self.playlist.bind(minimum_height=self.playlist.setter('height'))

        scrollbar = ScrollView(size_hint=(0.91, None), size=(self.playlist.width,
                               self.playlist.height), pos=(20, 100))

        self.background = Image(source='my_img/logo1.jpg', pos_hint={'center_x': 0.50, 'center_y': 0.73})

        self.song_info = Label(pos_hint={'center_x': 0.50, 'center_y': 0.48})

        self.play_button = MDIconButton(pos_hint={'center_x': 0.50, 'center_y': 0.05}, icon='my_img/play.png',
                                        on_press=self.play_music)

        self.playlist_button = MDIconButton(pos_hint={'center_x': 0.9, 'center_y': 0.05},
                                            icon='my_img/playlist.png', on_release=self.go_to_screen2)

        self.clear_music_playlist = MDIconButton(pos_hint={'center_x': 0.8, 'center_y': 0.05},
                                                 icon='my_img/clear_playlist.png',
                                                 on_release=self.clear_playlist)

        self.forward_button = MDIconButton(pos_hint={'center_x': 0.6, 'center_y': 0.05}, icon='my_img/next.png',
                                           on_press=self.next)

        self.back_button = MDIconButton(pos_hint={'center_x': 0.4, 'center_y': 0.05, }, icon='my_img/back.png',
                                        on_press=self.back)

        self.random_music = MDIconButton(pos_hint={'center_x': 0.7, 'center_y': 0.05}, icon='my_img/random.png',
                                         on_press=self.random)

        self.time_at_the_moment = Label(text='00:00', pos_hint={'center_x': 0.16, 'center_y': 0.095},
                                        size_hint=(1, 1), font_size=18)

        self.total_time = Label(text='00:00', pos_hint={'center_x': 0.84, 'center_y': 0.095},
                                size_hint=(1, 1), font_size=18)

        self.progressbar = ProgressBar(value=0, pos_hint={'center_x': 0.5, 'center_y': 0.12},
                                       size_hint=(0.8, 0.75))

        self.volume_slider = Slider(min=0, max=1, value=0.5, orientation='horizontal',
                                    pos_hint={'center_x': 0.2, 'center_y': 0.05}, size_hint=(0.3, 0.2))

        self.Second_window = Screen(size=(450, 700), name='second')

        my_layout_second = MDRelativeLayout(md_bg_color=[0, 0, 0, 0.8])

        self.playlist_second = MDGridLayout(cols=1, spacing=10, size_hint_y=None, md_bg_color=[255, 255, 255, 0.4],
                                            size=(100, 250))
        self.playlist_second.bind(minimum_height=self.playlist_second.setter('height'))

        scrollbar_second = ScrollView(size_hint=(0.91, None),
                                      size=(self.playlist_second.width, self.playlist_second.height), pos=(20, 380))

        my_music_playlist = MDGridLayout(cols=1, spacing=10, size_hint_y=None, md_bg_color=[255, 255, 255, 0.4],
                                         size=(100, 260))

        my_music_playlist.bind(minimum_height=my_music_playlist.setter('height'))

        scrollbar_my_music = ScrollView(size_hint=(0.91, None),
                                        size=(my_music_playlist.width, my_music_playlist.height), pos=(20, 50))

        self.name_colection_music = Label(text="Your songs", pos_hint={'center_x': 0.5, 'center_y': 0.48},
                                          font_size=22, bold=True)

        self.name_playlist_second = Label(text="Playlist", pos_hint={'center_x': 0.5, 'center_y': 0.94},
                                          font_size=22, bold=True)

        self.face_button = MDIconButton(pos_hint={'center_x': 0.1, 'center_y': 0.94},
                                        icon='my_img/face.png', on_release=self.go_to_main_screen)

        self.clear_music_playlist_second = MDIconButton(pos_hint={'center_x': 0.2, 'center_y': 0.94},
                                                        icon='my_img/clear_playlist_2.png',
                                                        on_release=self.clear_playlist2)

        self.add_to_playlist = MDIconButton(pos_hint={'center_x': 0.9, 'center_y': 0.94},
                                            icon='my_img/add.png', on_release=self.add_music_to_playlist)

        def command_volume(instance, volume):

            self.sound.volume = volume

        self.volume_slider.bind(value=command_volume)

        self.list_append_music = []

        for i in self.song_list:

            list_items = OneLineListItem(text=i, on_press=self.append_music)

            my_music_playlist.add_widget(list_items)

        # MY_LAYOUT_WIDGET
        self.Main_window.add_widget(self.my_layout)
        scrollbar.add_widget(self.playlist)
        self.my_layout.add_widget(scrollbar)
        self.my_layout.add_widget(self.play_button)
        self.my_layout.add_widget(self.playlist_button)
        self.my_layout.add_widget(self.clear_music_playlist)
        self.my_layout.add_widget(self.forward_button)
        self.my_layout.add_widget(self.back_button)
        self.my_layout.add_widget(self.time_at_the_moment)
        self.my_layout.add_widget(self.total_time)
        self.my_layout.add_widget(self.progressbar)
        self.my_layout.add_widget(self.volume_slider)
        self.my_layout.add_widget(self.random_music)
        self.my_layout.add_widget(self.background)
        self.my_layout.add_widget(self.song_info)

        self.window_manager.add_widget(self.Main_window)
        self.window_manager.add_widget(self.Second_window)

        # MY_LAYOUT_SECOND_WIDGET
        self.Second_window.add_widget(my_layout_second)
        scrollbar_second.add_widget(self.playlist_second)
        my_layout_second.add_widget(scrollbar_second)
        my_layout_second.add_widget(self.face_button)
        my_layout_second.add_widget(self.clear_music_playlist_second)
        my_layout_second.add_widget(self.add_to_playlist)
        my_layout_second.add_widget(self.name_colection_music)
        my_layout_second.add_widget(self.name_playlist_second)

        scrollbar_my_music.add_widget(my_music_playlist)
        my_layout_second.add_widget(scrollbar_my_music)

        return self.window_manager

    # def for Main window

    def play_music(self, obj):

        name = EasyID3(f'{self.music_dir}/{self.list_for_playlist[self.i]}')

        self.song_info.text = f" {name['artist'][0]} : {name['title'][0]}"

        if self.play_button.icon == 'my_img/play.png':

            self.my_layout.remove_widget(self.play_button)
            self.sound = SoundLoader.load(f'{self.music_dir}/{self.list_for_playlist[self.i]}')

            self.sound.play()
            self.play_button = MDIconButton(pos_hint={'center_x': 0.50, 'center_y': 0.05}, icon='my_img/stop.png',
                                            on_press=self.play_music)
            self.my_layout.add_widget(self.play_button)

            self.progressbar.max = self.sound.length
            self.progressbar_event = Clock.schedule_interval(self.update_progressbar, 1)
            self.set_time_event = Clock.schedule_interval(self.set_time, 1)

        elif self.play_button.icon == 'my_img/stop.png':
            self.sound.stop()
            self.my_layout.remove_widget(self.play_button)

            self.play_button = MDIconButton(pos_hint={'center_x': 0.50, 'center_y': 0.05}, icon='my_img/play.png',
                                            on_press=self.play_music)
            self.my_layout.add_widget(self.play_button)

            self.progressbar_event.cancel()
            self.set_time_event.cancel()
            self.progressbar.value = 0
            self.time_at_the_moment.text = '00:00'
            self.total_time.text = '00:00'

    def next(self, obj):

        self.sound.stop()

        self.progressbar_event.cancel()
        self.set_time_event.cancel()
        self.progressbar.value = 0
        self.time_at_the_moment.text = '00:00'
        self.total_time.text = '00:00'
        if self.i < len(self.list_for_playlist)-1:
            self.i += 1
            self.sound = SoundLoader.load(f'{self.music_dir}/{self.list_for_playlist[self.i]}')
            self.sound.play()

            self.progressbar.max = self.sound.length
            self.progressbar_event = Clock.schedule_interval(self.update_progressbar, 1)
            self.set_time_event = Clock.schedule_interval(self.set_time, 1)

            name = EasyID3(f'{self.music_dir}/{self.list_for_playlist[self.i]}')
            self.song_info.text = f" {name['artist'][0]} : {name['title'][0]}"

        elif self.i == len(self.list_for_playlist)-1:
            self.i = 0

            self.sound = SoundLoader.load(f'{self.music_dir}/{self.list_for_playlist[self.i]}')
            self.sound.play()

            self.progressbar.max = self.sound.length
            self.progressbar_event = Clock.schedule_interval(self.update_progressbar, 1)
            self.set_time_event = Clock.schedule_interval(self.set_time, 1)

            name = EasyID3(f'{self.music_dir}/{self.list_for_playlist[self.i]}')
            self.song_info.text = f" {name['artist'][0]} : {name['title'][0]}"

    def back(self, obj):
        self.sound.stop()
        self.progressbar_event.cancel()
        self.set_time_event.cancel()
        self.progressbar.value = 0
        self.time_at_the_moment.text = '00:00'
        self.total_time.text = '00:00'
        if self.i > 0:
            self.i -= 1

            self.sound = SoundLoader.load(f'{self.music_dir}/{self.list_for_playlist[self.i]}')
            self.sound.play()

            self.progressbar.max = self.sound.length
            self.progressbar_event = Clock.schedule_interval(self.update_progressbar, 1)
            self.set_time_event = Clock.schedule_interval(self.set_time, 1)

            name = EasyID3(f'{self.music_dir}/{self.list_for_playlist[self.i]}')
            self.song_info.text = f" {name['artist'][0]} : {name['title'][0]}"
        elif self.i == 0:
            self.i = len(self.list_for_playlist)-1

            self.sound = SoundLoader.load(f'{self.music_dir}/{self.list_for_playlist[self.i]}')
            self.sound.play()
            self.progressbar.max = self.sound.length
            self.progressbar_event = Clock.schedule_interval(self.update_progressbar, 1)
            self.set_time_event = Clock.schedule_interval(self.set_time, 1)

            name = EasyID3(f'{self.music_dir}/{self.list_for_playlist[self.i]}')
            self.song_info.text = f" {name['artist'][0]} : {name['title'][0]}"

    def random(self, obj):

        self.sound.stop()
        self.progressbar_event.cancel()
        self.set_time_event.cancel()
        self.progressbar.value = 0
        self.time_at_the_moment.text = '00:00'
        self.total_time.text = '00:00'

        var = random.randint(0, len(self.list_for_playlist)-1)

        self.sound = SoundLoader.load(f'{self.music_dir}/{self.list_for_playlist[var]}')
        self.progressbar.max = self.sound.length
        self.progressbar_event = Clock.schedule_interval(self.update_progressbar, 1)
        self.set_time_event = Clock.schedule_interval(self.set_time, 1)
        self.sound.play()

        name = EasyID3(f'{self.music_dir}/{self.list_for_playlist[var]}')
        self.song_info.text = f" {name['artist'][0]} : {name['title'][0]}"

    def update_progressbar(self, value):
        if self.progressbar.value <= self.sound.length:
            self.progressbar.value += 1

    def set_time(self, l):
        current_time = time.strftime('%M:%S', time.gmtime(self.progressbar.value))
        song_length = time.strftime('%M:%S', time.gmtime(self.sound.length))

        self.time_at_the_moment.text = current_time
        self.total_time.text = song_length

    def go_to_screen2(self, *args):
        self.root.current = 'second'

    def clear_playlist(self, obj):
        self.playlist.clear_widgets()
        self.list_for_playlist.clear()
        self.song_info.text = ""

    # def for second window

    def go_to_main_screen(self, *args):
        self.root.current = 'main'

    def append_music(self, obj):

        if obj.text not in self.list_append_music:
            self.list_append_music.append(obj.text)
            item = OneLineListItem(text=obj.text, on_press=self.on_pressed)
            self.playlist_second.add_widget(item)

    def on_pressed(self, obj):
        self.playlist_second.remove_widget(obj)
        self.list_append_music.remove(obj.text)

    def clear_playlist2(self, obj):
        self.playlist_second.clear_widgets()
        self.list_append_music.clear()

    def add_music_to_playlist(self, obj):

        for i in self.playlist_second.children[::-1]:
            name = EasyID3(f'{self.music_dir}/{i.text}')
            if i.text not in self.list_for_playlist:
                self.list_for_playlist.append(i.text)
                self.playlist.add_widget(OneLineListItem(text=f" {name['artist'][0]} : {name['title'][0]}"))


if __name__ == "__main__":
    MyApp().run()
