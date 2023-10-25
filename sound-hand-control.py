import cv2
import mediapipe as mp
import pyautogui
import time

mp_hands = mp.solutions.hands
cam = cv2.VideoCapture(0)
hand = mp_hands.Hands()

prev_landmarks = None
prev_time = 0
prev_skip_back_time = 0
prev_skip_for_time = 0

while True:
    data, image = cam.read()
    image = cv2.flip(image, 1)
    results = hand.process(image)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            if prev_landmarks:
                prev_x, prev_y = prev_landmarks[8].x, prev_landmarks[8].y
                cur_x, cur_y = hand_landmarks.landmark[8].x, hand_landmarks.landmark[8].y
                
                distance = cur_x - prev_x

                if distance < -0.1:
                    current_time = time.time() 
                    if current_time - prev_skip_back_time >= 3:
                        prev_skip_back_time=current_time
                        pyautogui.hotkey("prevtrack")
                        pyautogui.hotkey("prevtrack")
                        print('Previous Track')
                if distance > 0.1:
                    current_time = time.time()  
                    if current_time - prev_skip_for_time >= 3:
                        prev_skip_for_time = current_time
                        pyautogui.hotkey("nexttrack")
                        print('Next Track')
                
                if hand_landmarks.landmark[5].y < hand_landmarks.landmark[8].y and hand_landmarks.landmark[9].y < hand_landmarks.landmark[12].y and hand_landmarks.landmark[13].y < hand_landmarks.landmark[16].y and hand_landmarks.landmark[17].y < hand_landmarks.landmark[20].y and hand_landmarks.landmark[4].x < hand_landmarks.landmark[20].x:
                    current_time = time.time()
                    if current_time - prev_time >= 3:
                        pyautogui.hotkey("playpause")  
                        print('Pause')
                        prev_time = current_time
                            
            prev_landmarks = hand_landmarks.landmark

    cv2.imshow('handtrack', image)
    key = cv2.waitKey(1)

    if key == 27:  
        break

cv2.destroyAllWindows()
cam.release()