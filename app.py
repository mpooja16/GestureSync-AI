
import tkinter as tk
import cv2
import queue
from PIL import Image, ImageTk
from gesture_control import GestureController
from voice_control import VoiceController


class GestureAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VoiceMotion AI | Smart Control")
        self.root.geometry("1100x760")
        self.root.configure(bg="#101827")

        self.camera = None
        self.controller = None
        self.voice_controller = None
        self.running = False
        self.photo = None
        self.voice_messages = queue.Queue()

        header = tk.Frame(root, bg="#182438", padx=20, pady=16)
        header.pack(fill="x")

        tk.Label(
            header, text="VOICEMOTION AI",
            font=("Segoe UI", 23, "bold"),
            fg="#65e6c4", bg="#182438"
        ).pack(side="left")

        tk.Label(
            header, text="Voice + Gesture Computer Control",
            font=("Segoe UI", 11),
            fg="white", bg="#182438"
        ).pack(side="right")

        body = tk.Frame(root, bg="#101827", padx=20, pady=20)
        body.pack(fill="both", expand=True)

        self.video = tk.Label(
            body, text="Camera is stopped",
            font=("Segoe UI", 16),
            fg="white", bg="#202d42"
        )
        self.video.pack(
            side="left", fill="both", expand=True, padx=(0, 20)
        )

        panel = tk.Frame(body, bg="#182438", padx=18, pady=18)
        panel.pack(side="right", fill="y")

        tk.Label(
            panel, text="CONTROL PANEL",
            font=("Segoe UI", 15, "bold"),
            fg="#65e6c4", bg="#182438"
        ).pack(anchor="w", pady=(0, 12))

        self.status = tk.Label(
            panel, text="Camera OFF",
            fg="#ff8888", bg="#182438",
            font=("Segoe UI", 11, "bold")
        )
        self.status.pack(anchor="w")

        tk.Label(
            panel, text="DETECTED GESTURE",
            fg="#a9b8cf", bg="#182438",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", pady=(18, 5))

        self.gesture = tk.Label(
            panel, text="None",
            fg="white", bg="#182438",
            font=("Segoe UI", 17, "bold"),
            wraplength=240
        )
        self.gesture.pack(anchor="w")

        tk.Label(
            panel, text="LAST GESTURE ACTION",
            fg="#a9b8cf", bg="#182438",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", pady=(18, 5))

        self.action = tk.Label(
            panel, text="Waiting...",
            fg="white", bg="#182438",
            font=("Segoe UI", 10),
            wraplength=240
        )
        self.action.pack(anchor="w")

        tk.Label(
            panel, text="VOICE STATUS",
            fg="#a9b8cf", bg="#182438",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", pady=(18, 5))

        self.voice_status = tk.Label(
            panel, text="Voice OFF",
            fg="#ffcc80", bg="#182438",
            font=("Segoe UI", 10),
            wraplength=240,
            justify="left"
        )
        self.voice_status.pack(anchor="w")

        tk.Label(
            panel, text="VOICE ACTION",
            fg="#a9b8cf", bg="#182438",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", pady=(12, 5))

        self.voice_action = tk.Label(
            panel, text="Waiting for command",
            fg="white", bg="#182438",
            font=("Segoe UI", 10),
            wraplength=240,
            justify="left"
        )
        self.voice_action.pack(anchor="w")

        button_style = {
            "font": ("Segoe UI", 10, "bold"),
            "relief": "flat",
            "padx": 10,
            "pady": 9
        }

        tk.Button(
            panel, text="START CAMERA",
            command=self.start,
            bg="#65e6c4", fg="#101827",
            **button_style
        ).pack(fill="x", pady=(18, 6))

        tk.Button(
            panel, text="STOP CAMERA",
            command=self.stop,
            bg="#33445e", fg="white",
            **button_style
        ).pack(fill="x", pady=4)

        tk.Button(
            panel, text="START VOICE",
            command=self.start_voice,
            bg="#7c9cff", fg="#101827",
            **button_style
        ).pack(fill="x", pady=(12, 6))

        tk.Button(
            panel, text="STOP VOICE",
            command=self.stop_voice,
            bg="#33445e", fg="white",
            **button_style
        ).pack(fill="x", pady=4)

        tk.Label(
            panel,
            text="GESTURE GUIDE\n"
                 "Index finger: Move mouse\n"
                 "Pinch: Click\n"
                 "Open palm: Play/Pause\n"
                 "Two fingers: Next track\n"
                 "Fist: Previous track\n\n"
                 "VOICE COMMANDS\n"
                 "Say: Next track\n"
                 "Say: Previous track\n"
                 "Say: Play music\n"
                 "Say: Pause music",
            fg="#dce6f5", bg="#182438",
            font=("Segoe UI", 9), justify="left"
        ).pack(anchor="w", pady=(16, 0))

        tk.Label(
            root,
            text="Python • OpenCV • MediaPipe • SpeechRecognition",
            fg="#a9b8cf", bg="#101827", pady=10
        ).pack()

        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.after(100, self.check_voice_messages)

    def start(self):
        if self.running:
            return

        self.camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        if not self.camera.isOpened():
            self.camera.release()
            self.camera = None
            self.action.config(text="Cannot open camera.")
            return

        try:
            self.controller = GestureController()
        except Exception as error:
            self.camera.release()
            self.camera = None
            self.action.config(text=f"Could not start: {error}")
            return

        self.running = True
        self.status.config(text="Camera ON", fg="#65e6c4")
        self.update_frame()

    def update_frame(self):
        if not self.running:
            return

        success, frame = self.camera.read()

        if not success:
            self.action.config(text="Cannot read camera.")
            self.stop()
            return

        frame, gesture, message = self.controller.process_frame(frame)

        self.gesture.config(text=gesture)

        if message:
            self.action.config(text=message)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)
        image.thumbnail((680, 560))

        self.photo = ImageTk.PhotoImage(image)
        self.video.config(image=self.photo, text="")

        self.root.after(15, self.update_frame)

    def start_voice(self):
        if (
            self.voice_controller is not None
            and self.voice_controller.running
        ):
            self.voice_status.config(text="Voice is already running")
            return

        try:
            self.voice_controller = VoiceController(
                on_status=self.voice_messages.put
            )
            self.voice_controller.start()
            self.voice_status.config(
                text="Starting microphone...",
                fg="#65e6c4"
            )
        except Exception as error:
            self.voice_controller = None
            self.voice_status.config(
                text=f"Could not start voice: {error}",
                fg="#ff8888"
            )

    def stop_voice(self):
        if self.voice_controller is not None:
            self.voice_controller.stop()
            self.voice_controller = None

        self.voice_status.config(
            text="Voice OFF", fg="#ffcc80"
        )

    def check_voice_messages(self):
        try:
            while True:
                message = self.voice_messages.get_nowait()

                self.voice_status.config(text=message)

                if message.startswith("You said:"):
                    self.voice_action.config(
                        text="Recognized command: "
                             + message.split(":", 1)[1].strip()
                    )
                elif message.startswith("Voice action:"):
                    self.voice_action.config(
                        text=message
                    )
                elif message.startswith("Microphone error:"):
                    self.voice_status.config(
                        text=message, fg="#ff8888"
                    )
                elif "unavailable" in message.lower():
                    self.voice_status.config(
                        text=message, fg="#ff8888"
                    )

        except queue.Empty:
            pass

        if self.root.winfo_exists():
            self.root.after(100, self.check_voice_messages)

    def stop(self):
        self.running = False

        if self.camera is not None:
            self.camera.release()
            self.camera = None

        if self.controller is not None:
            self.controller.close()
            self.controller = None

        self.video.config(
            image="", text="Camera is stopped",
            bg="#202d42"
        )
        self.photo = None
        self.status.config(text="Camera OFF", fg="#ff8888")
        self.gesture.config(text="None")

    def close(self):
        self.stop_voice()
        self.stop()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = GestureAIApp(root)
    root.mainloop()
