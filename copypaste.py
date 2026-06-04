import cv2
import mediapipe as mp
import pyautogui
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

cap = cv2.VideoCapture(0)

copy_gesture = False
paste_gesture = False

last_action_time = 0
ACTION_COOLDOWN = 1

while True:
    ret, frame = cap.read()

    if not ret:
        continue

    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            thumb_tip = hand_landmarks.landmark[
                mp_hands.HandLandmark.THUMB_TIP
            ]

            index_tip = hand_landmarks.landmark[
                mp_hands.HandLandmark.INDEX_FINGER_TIP
            ]

            middle_tip = hand_landmarks.landmark[
                mp_hands.HandLandmark.MIDDLE_FINGER_TIP
            ]

            if (
                thumb_tip.y
                < hand_landmarks.landmark[
                    mp_hands.HandLandmark.THUMB_IP
                ].y
                < index_tip.y
            ):
                copy_gesture = True
            else:
                copy_gesture = False

            if (
                index_tip.y < thumb_tip.y
                and middle_tip.y < thumb_tip.y
            ):
                paste_gesture = True
            else:
                paste_gesture = False

            x = int(
                thumb_tip.x * frame.shape[1]
            )

            y = int(
                thumb_tip.y * frame.shape[0]
            )

            pyautogui.moveTo(x, y)

            current_time = time.time()

            if (
                copy_gesture
                and current_time - last_action_time
                > ACTION_COOLDOWN
            ):
                pyautogui.hotkey("ctrl", "c")
                last_action_time = current_time

            if (
                paste_gesture
                and current_time - last_action_time
                > ACTION_COOLDOWN
            ):
                pyautogui.hotkey("ctrl", "v")
                last_action_time = current_time

    cv2.imshow(
        "Gesture Control",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

hands.close()
cap.release()
cv2.destroyAllWindows()