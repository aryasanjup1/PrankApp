import random
import os
import threading
from kivy.app import App
from kivy.uix.image import AsyncImage
from kivy.uix.widget import Widget
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle
from plyer import vibrator
from kivy.utils import platform

# APK-Compatible Asset Path
def resource_path(relative_path):
    if platform == 'android':
        from android.storage import app_storage_path
        return os.path.join(app_storage_path(), relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)

class PrankScreen(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Flashing background effect
        with self.canvas.before:
            self.flash_color = Color(1, 1, 1, 0)
            self.flash_rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_rect, pos=self.update_rect)

        # **One widget to handle both GIFs and images properly**
        self.image_widget = AsyncImage(size=self.size, allow_stretch=True, keep_ratio=False)
        self.add_widget(self.image_widget)

        # Load bundled assets inside APK
        self.all_images = self.get_files(resource_path("assets/"), [".jpg", ".png", ".gif"])
        self.sound_paths = self.get_files(resource_path("assets/"), [".mp3"])

        if not self.all_images:
            print("⚠ No images or GIFs found!")
        if not self.sound_paths:
            print("⚠ No sounds found!")

        # **Start chaos**
        Clock.schedule_interval(self.switch_media, 0.3)  # **Switch images/GIFs properly**
        Clock.schedule_interval(self.start_sound_thread, 0.5)  # **Overlapping sounds**
        Clock.schedule_interval(self.screen_shake, 0.2)  # **Smoother shaking**
        Clock.schedule_interval(self.flash_effect, 0.3)  # **Flashing effect**

        self.switch_media(0)  # Start with a random image/GIF

    def update_rect(self, *args):
        """Updates screen flashing effect to match window size."""
        self.flash_rect.size = self.size
        self.flash_rect.pos = self.pos
        self.image_widget.size = self.size  # Ensures full-screen images & GIFs

    def get_files(self, path, exts):
        """Finds all files with given extensions inside APK."""
        try:
            return [os.path.join(path, f) for f in os.listdir(path) if f.lower().endswith(tuple(exts))]
        except Exception:
            return []  # Prevents crashes if folder is missing

    def switch_media(self, dt):
        """Switches between images & GIFs properly without freezing."""
        if self.all_images:
            # **Show random image or GIF**
            self.image_widget.source = random.choice(self.all_images)

    def start_sound_thread(self, dt):
        """Starts a separate thread for playing sounds to prevent lag."""
        if self.sound_paths:
            threading.Thread(target=self.play_sound, daemon=True).start()

    def play_sound(self):
        """Plays overlapping sounds without lag."""
        try:
            sound = SoundLoader.load(random.choice(self.sound_paths))
            if sound:
                sound.volume = random.uniform(0.5, 1.5)  # Random loudness
                sound.play()
        except Exception as e:
            print(f"⚠ Sound error: {e}")

        # Try to vibrate (if supported)
        try:
            pattern = [random.randint(50, 300) for _ in range(5)]
            vibrator.vibrate(pattern)
        except Exception:
            pass  # Ignore errors if vibration isn't available

    def screen_shake(self, dt):
        """Creates a smooth but insane screen shaking effect."""
        random_x = random.randint(-80, 80)
        random_y = random.randint(-80, 80)

        anim = Animation(pos=(random_x, random_y), duration=0.1)  # Smoother shaking
        anim.start(self)

    def flash_effect(self, dt):
        """Ultra flashing effect with random colors."""
        self.flash_color.rgb = [random.random(), random.random(), random.random()]  # Crazy colors
        self.flash_color.a = random.choice([0, 0.3, 0.6, 1])  # Transparency variations

class PrankApp(App):
    def build(self):
        return PrankScreen()

PrankApp().run()