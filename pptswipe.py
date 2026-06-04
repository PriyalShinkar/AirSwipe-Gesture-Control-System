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

SWIPE_DISTANCE_THRESHOLD = 100

swipe_left = False
swipe_right = False

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

            index_tip_x = int(
                index_tip.x * screen_width
            )

            index_tip_y = int(
                index_tip.y * screen_height
            )

            thumb_tip_x = int(
                thumb_tip.x * screen_width
            )

            thumb_tip_y = int(
                thumb_tip.y * screen_height
            )

            # Previous Slide
            if (
                thumb_tip_x
                < index_tip_x - SWIPE_DISTANCE_THRESHOLD
            ):

                if (
                    not swipe_left
                    and time.time() - action_time > 1
                ):
                    pyautogui.press("left")

                    swipe_left = True
                    action_time = time.time()

            else:
                swipe_left = False

            # Next Slide
            if (
                thumb_tip_x
                > index_tip_x + SWIPE_DISTANCE_THRESHOLD
            ):

                if (
                    not swipe_right
                    and time.time() - action_time > 1
                ):
                    pyautogui.press("right")

                    swipe_right = True
                    action_time = time.time()

            else:
                swipe_right = False

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