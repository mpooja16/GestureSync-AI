# GestureSync AI
### Voice and Hand Gesture-Based Desktop Automation

GestureSync AI is a Python-based desktop automation project that allows users to interact with their computer using **hand gestures and voice commands**. It combines computer vision and speech recognition to provide a touchless way to control common desktop actions.

## 🚀 Project Overview

Traditional computer interaction depends mainly on a keyboard and mouse. GestureSync AI explores an alternative by enabling users to control selected computer functions through webcam-based hand tracking and spoken commands.

The system detects hand movements through a webcam and recognizes supported voice commands through a microphone. These inputs are translated into desktop actions.

## 🎯 Objectives

- Enable mouse movement using hand gestures.
- Support pinch gestures for mouse clicking.
- Execute supported desktop actions using voice commands.
- Combine gesture and voice interaction in one application.
- Explore accessible, touchless human-computer interaction.

## ✨ Key Features

- **Hand Tracking:** Detects hand landmarks using MediaPipe.
- **Gesture-Based Mouse Control:** Moves the cursor using the index finger.
- **Pinch-to-Click:** Uses a pinch gesture to trigger a mouse click.
- **Voice Commands:** Recognizes supported spoken instructions.
- **Desktop Automation:** Performs configured actions using PyAutoGUI.
- **Web Navigation:** Opens configured websites using Python's webbrowser module.
- **Graphical Interface:** Provides an application interface using Tkinter.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| OpenCV | Webcam and image processing |
| MediaPipe | Hand landmark detection |
| SpeechRecognition | Speech input recognition |
| PyAutoGUI | Mouse and keyboard automation |
| Tkinter | Desktop graphical interface |
| Threading | Runs voice listening separately from the main interface |
| Webbrowser | Opens websites |

## 🏗️ System Architecture

```text
         USER INPUT
         /        \
        /          \
  Webcam Input   Microphone Input
       |                |
  OpenCV Camera   Speech Recognition
       |                |
  MediaPipe       Recognized Text
  Hand Tracking        |
       |          Command Matching
  Gesture Logic        |
       |          Voice Action Logic
       |                |
       +-------+--------+
               |
        Desktop Actions
               |
     Mouse / Keyboard / Websites
```

## ⚙️ How It Works

1. The application starts and initializes the webcam and voice controller.
2. OpenCV captures frames from the webcam.
3. MediaPipe detects hand landmarks in the video frames.
4. The gesture controller interprets hand positions and recognizes supported gestures.
5. The voice controller listens for speech and converts recognized speech into text.
6. The relevant controller maps each supported gesture or voice command to an action.
7. PyAutoGUI or the webbrowser module performs the configured desktop action.

## 💻 Installation and Setup

### Prerequisites

- Python 3.12 (recommended for this project setup)
- Webcam
- Microphone
- Windows desktop or laptop

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/GestureSync-AI.git
cd GestureSync-AI
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

Use the actual entry-point filename if your application starts from a different file.

## 🧪 Testing

The following functions were tested during development:

- Webcam initialization
- Index-finger mouse movement
- Pinch-to-click interaction
- Voice-listening initialization
- Recognition of the tested "next track" voice command

Additional commands should be documented as tested only after they work successfully in the final application.

## 🔮 Future Enhancements

- Expand the number of supported natural-language voice commands.
- Add more configurable hand gestures.
- Improve speech recognition in noisy environments.
- Add customizable gesture-to-action mappings.
- Improve error handling and user feedback.
- Support additional operating systems where dependencies permit.

## 🎓 Project Domain

Artificial Intelligence | Computer Vision | Speech Recognition | Human-Computer Interaction | Desktop Automation

## 👩‍💻 Author

**Pooja M**

Final-year B.Tech — Artificial Intelligence and Data Science

## 📌 Note

This project is intended for learning and demonstrating touchless desktop interaction. Camera and microphone access, internet connectivity for applicable speech-recognition services, and operating-system permissions may be required.
