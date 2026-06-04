import cv2
import mediapipe as mp
import pyautogui
import time

mp_hand = mp.solutions.hands
hands = mp_hand.Hands()

cap = cv2.VideoCapture(0)

THUMB_TIP = 4
INDEX_FINGER_TIP = 8
MIDDLE_FINGER_TIP = 12

PINCH_IN_DISTANCE_THRESHOLD = 30

pinch_in_gesture = False

last_zoom_time = 0
ZOOM_COOLDOWN = 1

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

            thumb_tip = hand_landmarks.landmark[
                THUMB_TIP
            ]

            index_tip = hand_landmarks.landmark[
                INDEX_FINGER_TIP
            ]

            middle_tip = hand_landmarks.landmark[
                MIDDLE_FINGER_TIP
            ]

            thumb_tip_x = int(
                thumb_tip.x * frame.shape[1]
            )

            thumb_tip_y = int(
                thumb_tip.y * frame.shape[0]
            )

            index_tip_x = int(
                index_tip.x * frame.shape[1]
            )

            index_tip_y = int(
                index_tip.y * frame.shape[0]
            )

            middle_tip_x = int(
                middle_tip.x * frame.shape[1]
            )

            middle_tip_y = int(
                middle_tip.y * frame.shape[0]
            )

            distance_thumb_index = int(
                (
                    (thumb_tip_x - index_tip_x) ** 2
                    + (thumb_tip_y - index_tip_y) ** 2
                ) ** 0.5
            )

            distance_thumb_middle = int(
                (
                    (thumb_tip_x - middle_tip_x) ** 2
                    + (thumb_tip_y - middle_tip_y) ** 2
                ) ** 0.5
            )

            if (
                distance_thumb_index
                < PINCH_IN_DISTANCE_THRESHOLD
                and distance_thumb_middle
                < PINCH_IN_DISTANCE_THRESHOLD
            ):

                current_time = time.time()

                if (
                    not pinch_in_gesture
                    and current_time - last_zoom_time
                    > ZOOM_COOLDOWN
                ):
                    pyautogui.hotkey("ctrl", "add")

                    pinch_in_gesture = True
                    last_zoom_time = current_time

            else:
                pinch_in_gesture = False

            mp.solutions.drawing_utils.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hand.HAND_CONNECTIONS
            )

    cv2.imshow(
        "Hand Gesture Zoom In",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

hands.close()
cap.release()
cv2.destroyAllWindows()