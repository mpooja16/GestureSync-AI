
import speech_recognition as sr
import threading
import pyautogui
import os
import time
import webbrowser
import subprocess
from datetime import datetime


class VoiceController:
    def __init__(self, on_status=None):
        self.recognizer = sr.Recognizer()
        self.on_status = on_status or print
        self.running = False
        self.worker = None

        self.project_folder = os.path.dirname(
            os.path.abspath(__file__)
        )
        self.screenshot_folder = os.path.join(
            self.project_folder, "screenshots"
        )
        os.makedirs(self.screenshot_folder, exist_ok=True)

        # 80 spoken phrases mapped to their actions.
        # Multiple phrases can trigger the same action.
        self.commands = {}

        def add(action, phrases):
            for phrase in phrases:
                self.commands[phrase] = action

        # 1-16: Music and volume
        add("next_track", [
            "next track", "next song", "play next song"
        ])
        add("previous_track", [
            "previous track", "previous song",
            "play previous song"
        ])
        add("toggle_music", [
            "play music", "pause music",
            "resume music", "toggle music"
        ])
        add("volume_up", ["volume up", "increase volume"])
        add("volume_down", ["volume down", "decrease volume"])
        add("mute", ["mute sound"])
        add("unmute", ["unmute sound"])

        # 17-30: Websites
        add("chrome", ["open chrome", "open browser"])
        add("youtube", ["open youtube", "go to youtube"])
        add("google", ["open google", "search google"])
        add("gmail", ["open gmail"])
        add("chatgpt", ["open chatgpt"])
        add("github", ["open github"])
        add("facebook", ["open facebook"])
        add("instagram", ["open instagram"])
        add("wikipedia", ["open wikipedia"])
        add("maps", ["open google maps"])
        add("amazon", ["open amazon"])
        add("spotify", ["open spotify"])
        add("zoom", ["open zoom"])
        add("teams", ["open teams"])

        # 31-40: Applications
        add("notepad", ["open notepad"])
        add("calculator", ["open calculator"])
        add("explorer", ["open file explorer"])
        add("downloads", ["open downloads folder"])
        add("cmd", ["open command prompt"])
        add("settings", ["open settings"])
        add("paint", ["open paint"])
        add("excel", ["open excel"])
        add("word", ["open word"])
        add("vscode", ["open vs code"])

        # 41-54: Keyboard commands
        add("copy", ["copy", "copy that"])
        add("paste", ["paste"])
        add("cut", ["cut"])
        add("undo", ["undo"])
        add("redo", ["redo"])
        add("select_all", ["select all"])
        add("save", ["save file"])
        add("enter", ["press enter"])
        add("escape", ["press escape"])
        add("tab", ["press tab"])
        add("backspace", ["press backspace"])
        add("delete", ["delete this"])
        add("newline", ["new line"])
        add("screenshot", ["take screenshot"])

        # 55-68: Browser and window navigation
        add("new_tab", ["new tab"])
        add("close_tab", ["close tab"])
        add("reopen_tab", ["reopen tab"])
        add("refresh", ["refresh page"])
        add("back", ["go back"])
        add("forward", ["go forward"])
        add("scroll_down", ["scroll down"])
        add("scroll_up", ["scroll up"])
        add("top", ["go to top"])
        add("bottom", ["go to bottom"])
        add("switch_window", ["switch window"])
        add("minimize", ["minimize window"])
        add("maximize", ["maximize window"])
        add("close_window", ["close window"])

        # 69-80: Utilities
        add("lock", ["lock computer"])
        add("desktop", ["show desktop"])
        add("zoom_in", ["zoom in"])
        add("zoom_out", ["zoom out"])
        add("task_manager", ["open task manager"])
        add("time", ["tell me the time"])
        add("stop", ["stop voice", "stop voice control"])
        add("clear_address", ["clear screen"])
        add("search_python", ["search google for python tutorials"])
        add("search_tamil", ["search youtube for tamil songs"])
        add("first_video", ["play the first video"])
        add("search_google_dynamic", ["search google for"])

    def start(self):
        if self.running:
            return

        self.running = True
        self.worker = threading.Thread(
            target=self._listen_loop,
            daemon=True
        )
        self.worker.start()
        self.on_status("Voice control starting...")

    def stop(self):
        self.running = False
        self.on_status("Voice control stopped.")

    def _listen_loop(self):
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(
                    source, duration=1
                )
                self.on_status("Listening for voice commands...")

                while self.running:
                    try:
                        audio = self.recognizer.listen(
                            source,
                            timeout=1,
                            phrase_time_limit=5
                        )
                        command = self.recognizer.recognize_google(
                            audio
                        ).lower().strip()

                        self.on_status(f"You said: {command}")
                        self._handle_command(command)

                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError:
                        self.on_status(
                            "Speech service unavailable. Check internet."
                        )
                        time.sleep(1)

        except (OSError, AttributeError) as error:
            self.on_status(f"Microphone error: {error}")
        finally:
            self.running = False

    def _open_app(self, target):
        try:
            subprocess.Popen(
                ["cmd", "/c", "start", "", target],
                creationflags=getattr(
                    subprocess, "CREATE_NO_WINDOW", 0
                )
            )
            self.on_status(f"Voice action: Opening {target}")
        except Exception as error:
            self.on_status(f"Could not open {target}: {error}")

    def _open_url(self, url, label):
        webbrowser.open(url)
        self.on_status(f"Voice action: Opening {label}")

    def _handle_command(self, command):
        # Search phrases can include words after the trigger.
        if command.startswith("search google for "):
            query = command[len("search google for "):].strip()
            if query:
                self._open_url(
                    "https://www.google.com/search?q="
                    + __import__("urllib.parse").parse.quote(query),
                    "Google search"
                )
            return

        if command.startswith("search youtube for "):
            query = command[len("search youtube for "):].strip()
            if query:
                self._open_url(
                    "https://www.youtube.com/results?search_query="
                    + __import__("urllib.parse").parse.quote(query),
                    "YouTube search"
                )
            return

        action = self.commands.get(command)

        if action is None:
            self.on_status("Command not recognized. Try again.")
            return

        try:
            if action == "next_track":
                pyautogui.press("nexttrack")

            elif action == "previous_track":
                pyautogui.press("prevtrack")

            elif action == "toggle_music":
                pyautogui.press("playpause")

            elif action == "volume_up":
                pyautogui.press("volumeup")

            elif action == "volume_down":
                pyautogui.press("volumedown")

            elif action == "mute":
                pyautogui.press("volumemute")

            elif action == "unmute":
                pyautogui.press("volumemute")

            elif action == "chrome":
                self._open_app("chrome")

            elif action == "youtube":
                self._open_url("https://www.youtube.com", "YouTube")

            elif action == "google":
                self._open_url("https://www.google.com", "Google")

            elif action == "gmail":
                self._open_url("https://mail.google.com", "Gmail")

            elif action == "chatgpt":
                self._open_url("https://chatgpt.com", "ChatGPT")

            elif action == "github":
                self._open_url("https://github.com", "GitHub")

            elif action == "facebook":
                self._open_url("https://www.facebook.com", "Facebook")

            elif action == "instagram":
                self._open_url("https://www.instagram.com", "Instagram")

            elif action == "wikipedia":
                self._open_url("https://www.wikipedia.org", "Wikipedia")

            elif action == "maps":
                self._open_url("https://maps.google.com", "Google Maps")

            elif action == "amazon":
                self._open_url("https://www.amazon.in", "Amazon")

            elif action == "spotify":
                self._open_url("https://open.spotify.com", "Spotify")

            elif action == "zoom":
                self._open_url("https://zoom.us", "Zoom")

            elif action == "teams":
                self._open_url("https://teams.microsoft.com", "Teams")

            elif action == "notepad":
                self._open_app("notepad")

            elif action == "calculator":
                self._open_app("calc")

            elif action == "explorer":
                self._open_app("explorer")

            elif action == "downloads":
                os.startfile(os.path.join(
                    os.path.expanduser("~"), "Downloads"
                ))

            elif action == "cmd":
                self._open_app("cmd")

            elif action == "settings":
                os.startfile("ms-settings:")

            elif action == "paint":
                self._open_app("mspaint")

            elif action == "excel":
                self._open_app("excel")

            elif action == "word":
                self._open_app("winword")

            elif action == "vscode":
                self._open_app("code")

            elif action in {
                "copy", "paste", "cut", "undo", "redo",
                "select_all", "save", "enter", "escape",
                "tab", "backspace", "delete", "newline",
                "new_tab", "close_tab", "reopen_tab",
                "refresh", "back", "forward", "switch_window",
                "minimize", "maximize", "close_window",
                "desktop", "zoom_in", "zoom_out"
            }:
                keys = {
                    "copy": ("ctrl", "c"),
                    "paste": ("ctrl", "v"),
                    "cut": ("ctrl", "x"),
                    "undo": ("ctrl", "z"),
                    "redo": ("ctrl", "y"),
                    "select_all": ("ctrl", "a"),
                    "save": ("ctrl", "s"),
                    "enter": ("enter",),
                    "escape": ("esc",),
                    "tab": ("tab",),
                    "backspace": ("backspace",),
                    "delete": ("delete",),
                    "newline": ("enter",),
                    "new_tab": ("ctrl", "t"),
                    "close_tab": ("ctrl", "w"),
                    "reopen_tab": ("ctrl", "shift", "t"),
                    "refresh": ("ctrl", "r"),
                    "back": ("alt", "left"),
                    "forward": ("alt", "right"),
                    "switch_window": ("alt", "tab"),
                    "minimize": ("win", "down"),
                    "maximize": ("win", "up"),
                    "close_window": ("alt", "f4"),
                    "desktop": ("win", "d"),
                    "zoom_in": ("ctrl", "+"),
                    "zoom_out": ("ctrl", "-")
                }
                pyautogui.hotkey(*keys[action])

            elif action == "scroll_down":
                pyautogui.scroll(-5)

            elif action == "scroll_up":
                pyautogui.scroll(5)

            elif action == "top":
                pyautogui.press("home")

            elif action == "bottom":
                pyautogui.press("end")

            elif action == "screenshot":
                filename = "screenshot_" + datetime.now().strftime(
                    "%Y%m%d_%H%M%S"
                ) + ".png"
                filepath = os.path.join(
                    self.screenshot_folder, filename
                )
                pyautogui.screenshot().save(filepath)
                self.on_status(f"Screenshot saved: {filename}")
                return

            elif action == "lock":
                import ctypes
                ctypes.windll.user32.LockWorkStation()

            elif action == "task_manager":
                self._open_app("taskmgr")

            elif action == "time":
                self.on_status(
                    "Current time: "
                    + datetime.now().strftime("%I:%M %p")
                )
                return

            elif action == "clear_address":
                pyautogui.hotkey("ctrl", "l")

            elif action == "search_python":
                self._open_url(
                    "https://www.google.com/search?q=Python+tutorials",
                    "Python tutorials"
                )

            elif action == "search_tamil":
                self._open_url(
                    "https://www.youtube.com/results?search_query=Tamil+songs",
                    "Tamil songs"
                )

            elif action == "first_video":
                self._open_url(
                    "https://www.youtube.com",
                    "YouTube"
                )

            elif action == "search_google_dynamic":
                self._open_url("https://www.google.com", "Google")

            elif action == "stop":
                self.stop()
                return

            self.on_status(f"Voice action completed: {action}")

        except Exception as error:
            self.on_status(f"Action failed: {error}")
