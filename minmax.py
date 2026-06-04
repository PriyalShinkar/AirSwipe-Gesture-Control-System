import cv2
import mediapipe as mp
import pygetwindow as gw

mp_hand = mp.solutions.hands
hands = mp_hand.Hands()

cap = cv2.VideoCapture(0)

THUMB_TIP = 4
INDEX_FINGER_TIP = 8

OPEN_FIST_DISTANCE_THRESHOLD = 60
FIST_DISTANCE_THRESHOLD = 30

open_fist_gesture = False
fist_gesture = False

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

            distance = int(
                (
                    (thumb_tip_x - index_tip_x) ** 2
                    + (thumb_tip_y - index_tip_y) ** 2
                ) ** 0.5
            )

            # Minimize Window
            if distance > OPEN_FIST_DISTANCE_THRESHOLD:

                if not open_fist_gesture:

                    active_window = gw.getActiveWindow()

                    if active_window:
                        active_window.minimize()

                    open_fist_gesture = True
                    fist_gesture = False

            else:
                open_fist_gesture = False

            # Maximize Window
            if distance < FIST_DISTANCE_THRESHOLD:

                if not fist_gesture:

                    active_window = gw.getActiveWindow()

                    if active_window:
                        active_window.maximize()

                    fist_gesture = True
                    open_fist_gesture = False

            else:
                fist_gesture = False

            mp.solutions.drawing_utils.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hand.HAND_CONNECTIONS
            )

    cv2.imshow(
        "Hand Gesture Control",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

hands.close()
cap.release()
cv2.destroyAllWindows()