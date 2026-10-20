
import cv2
import mediapipe as mp
import pyautogui
import math
import time


class GestureController:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        self.screen_width, self.screen_height = pyautogui.size()
        self.pinch_active = False
        self.last_action_time = 0
        self.last_action = None
        self.gesture_delay = 1.2

        pyautogui.FAILSAFE = True

    @staticmethod
    def finger_up(hand, tip, pip):
        return hand.landmark[tip].y < hand.landmark[pip].y

    def process_frame(self, frame):
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        gesture = "No hand detected"
        action_message = None

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]

            self.mp_draw.draw_landmarks(
                frame, hand, self.mp_hands.HAND_CONNECTIONS
            )

            index = hand.landmark[8]
            thumb = hand.landmark[4]

            mouse_x = int(index.x * self.screen_width)
            mouse_y = int(index.y * self.screen_height)
            pyautogui.moveTo(mouse_x, mouse_y, duration=0.01)

            distance = math.hypot(
                index.x - thumb.x,
                index.y - thumb.y
            )

            if distance < 0.05:
                gesture = "PINCH - CLICK"
                if not self.pinch_active:
                    pyautogui.click()
                    action_message = "Mouse clicked"
                    self.pinch_active = True
            else:
                self.pinch_active = False

            index_up = self.finger_up(hand, 8, 6)
            middle_up = self.finger_up(hand, 12, 10)
            ring_up = self.finger_up(hand, 16, 14)
            pinky_up = self.finger_up(hand, 20, 18)

            action = None

            if index_up and middle_up and ring_up and pinky_up:
                gesture = "OPEN PALM"
                action = "playpause"
            elif index_up and middle_up and not ring_up and not pinky_up:
                gesture = "TWO FINGERS"
                action = "nexttrack"
            elif not any([index_up, middle_up, ring_up, pinky_up]):
                gesture = "FIST"
                action = "prevtrack"

            now = time.time()

            if action is None:
                self.last_action = None
            elif (
                action != self.last_action
                and now - self.last_action_time > self.gesture_delay
            ):
                pyautogui.press(action)
                self.last_action_time = now
                self.last_action = action

                messages = {
                    "playpause": "Play / Pause command sent",
                    "nexttrack": "Next track command sent",
                    "prevtrack": "Previous track command sent"
                }
                action_message = messages[action]

        cv2.putText(
            frame, gesture, (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8,
            (0, 255, 180), 2
        )

        return frame, gesture, action_message

    def close(self):
        self.hands.close()
