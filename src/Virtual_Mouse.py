import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# Screen size
screen_w, screen_h = pyautogui.size()

# Setup MediaPipe
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, model_complexity=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Click state
clicking_left = False
clicking_right = False
prev_x, prev_y = None, None
sensitivity = 2.5  # increase for faster movement

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    h, w, _ = frame.shape

    if results.multi_hand_landmarks and results.multi_handedness:
        hand_label = results.multi_handedness[0].classification[0].label
        if hand_label != "Right":
            cv2.putText(frame, "Left hand ignored", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (100, 100, 255), 3)
            prev_x, prev_y = None, None  # reset relative tracking
            if cv2.waitKey(1) & 0xFF == 27:
                break
            continue

        for hand_landmarks in results.multi_hand_landmarks:
            lm = hand_landmarks.landmark

            def is_finger_up(tip, pip):
                return lm[tip].y < lm[pip].y

            index_up = is_finger_up(8, 6)
            middle_up = is_finger_up(12, 10)
            thumb_up = lm[4].x > lm[3].x
            thumb_closed = not thumb_up

            x, y = int(lm[8].x * w), int(lm[8].y * h)

            # Debug text
            state_text = f"Index: {'Up' if index_up else 'Down'} | Middle: {'Up' if middle_up else 'Down'} | Thumb: {'Open' if thumb_up else 'Closed'}"
            cv2.putText(frame, state_text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 3)

            # ===== Mouse MOVE (relative) =====
            if index_up and middle_up and thumb_closed:
                if prev_x is not None and prev_y is not None:
                    dx = (x - prev_x) * sensitivity
                    dy = (y - prev_y) * sensitivity
                    pyautogui.moveRel(dx, dy, duration=0.01)
                    cv2.putText(frame, "MOVE", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (255, 255, 255), 4)
                prev_x, prev_y = x, y
            else:
                prev_x, prev_y = None, None

            # ===== LEFT CLICK =====
            if not index_up and middle_up and thumb_closed:
                if not clicking_left:
                    pyautogui.click()
                    clicking_left = True
                    print("✅ Left Click Triggered")
                    cv2.putText(frame, "LEFT CLICK", (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 255, 0), 4)
            else:
                clicking_left = False

            # ===== RIGHT CLICK =====
            if index_up and not middle_up and thumb_closed:
                if not clicking_right:
                    pyautogui.rightClick()
                    clicking_right = True
                    print("✅ Right Click Triggered")
                    cv2.putText(frame, "RIGHT CLICK", (10, 170), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 255), 4)
            else:
                clicking_right = False

            # ===== SCROLL UP =====
            if not index_up and not middle_up and thumb_up:
                pyautogui.scroll(40)
                cv2.putText(frame, "SCROLL UP", (10, 210), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (255, 255, 0), 4)

            # ===== SCROLL DOWN =====
            if index_up and middle_up and thumb_up:
                pyautogui.scroll(-40)
                cv2.putText(frame, "SCROLL DOWN", (10, 250), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 255, 255), 4)

            # Draw hand landmarks
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    else:
        prev_x, prev_y = None, None
        cv2.putText(frame, "No hand detected", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (128, 128, 128), 3)

    cv2.imshow("Virtual Mouse - macOS", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
