
import cv2
from gesture_control import GestureController


def main():
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not camera.isOpened():
        print("Cannot open camera. Close other camera apps and try again.")
        return

    controller = GestureController()

    try:
        print("Gesture AI started!")
        print("Press Q to quit.")

        while True:
            success, frame = camera.read()

            if not success:
                print("Cannot read camera.")
                break

            frame, gesture, message = controller.process_frame(frame)

            if message:
                print(message)

            cv2.imshow("Gesture AI - Mouse and Media Control", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        camera.release()
        controller.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
