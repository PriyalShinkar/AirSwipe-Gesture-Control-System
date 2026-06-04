import cv2
import mediapipe as mp
import pyautogui
import time

# Settings
pyautogui.PAUSE = 0.1

mp_hand = mp.solutions.hands
hands = mp_hand.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)

screen_width, screen_height = pyautogui.size()

INDEX_FINGER_TIP = 8
THUMB_TIP = 4

SCROLL_DISTANCE_THRESHOLD = 20
scroll_speed = 75

scroll_up = False
scroll_down = False

action_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            index_tip = hand_landmarks.landmark[
                INDEX_FINGER_TIP
            ]

            thumb_tip = hand_landmarks.landmark[
                THUMB_TIP
            ]

            index_tip_y = int(
                index_tip.y * screen_height
            )

            thumb_tip_y = int(
                thumb_tip.y * screen_height
            )

            # Scroll Up
            if (
                index_tip_y < thumb_tip_y
                and thumb_tip_y - index_tip_y
                > SCROLL_DISTANCE_THRESHOLD
            ):

                if (
                    not scroll_up
                    and time.time() - action_time > 0.1
                ):
                    pyautogui.scroll(scroll_speed)

                    scroll_up = True
                    action_time = time.time()

            else:
                scroll_up = False

            # Scroll Down
            if (
                thumb_tip_y < index_tip_y
                and index_tip_y - thumb_tip_y
                > SCROLL_DISTANCE_THRESHOLD
            ):

                if (
                    not scroll_down
                    and time.time() - action_time > 0.1
                ):
                    pyautogui.scroll(-scroll_speed)

                    scroll_down = True
                    action_time = time.time()

            else:
                scroll_down = False

            mp.solutions.drawing_utils.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hand.HAND_CONNECTIONS
            )

    cv2.imshow(
        "Gesture Control",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

hands.close()
cap.release()
cv2.destroyAllWindows()