import cv2
import numpy as np
import pyautogui
from pynput.mouse import Button, Controller
import math
import time
import random

mouse = Controller()
pyautogui.FAILSAFE = False
screen_width, screen_height = pyautogui.size()

lower_skin = np.array([0, 30, 60])
upper_skin = np.array([20, 150, 255])

def count_fingers(contour):
    hull = cv2.convexHull(contour, returnPoints=False)
    defects = cv2.convexityDefects(contour, hull)
    if defects is not None:
        count_defects = 0
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(contour[s][0])
            end = tuple(contour[e][0])
            far = tuple(contour[f][0])
            angle = math.degrees(math.atan2(end[1] - far[1], end[0] - far[0]) - math.atan2(start[1] - far[1], start[0] - far[0]))
            if angle <= 90:
                count_defects += 1
        return count_defects + 1
    return 0

cap = cv2.VideoCapture(0)

last_left = 0
last_right = 0
smooth_x = 320
smooth_y = 240

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5,5), np.uint8))
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(max_contour) > 10000:
            M = cv2.moments(max_contour)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            smooth_x = 0.7 * smooth_x + 0.3 * cx
            smooth_y = 0.7 * smooth_y + 0.3 * cy
            pyautogui.moveTo(int(smooth_x * screen_width / frame.shape[1]), int(smooth_y * screen_height / frame.shape[0] * 0.8))
            cv2.circle(frame, (int(smooth_x), int(smooth_y)), 10, (0, 255, 0), -1)
            
            fingers = count_fingers(max_contour)
            cv2.putText(frame, f'Fingers: {fingers}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            now = time.time()
            if fingers == 1 and now - last_left > 0.5:
                last_left = now
                mouse.press(Button.left)
                mouse.release(Button.left)
                cv2.putText(frame, 'Left Click', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            elif fingers == 2 and now - last_right > 0.5:
                last_right = now
                mouse.press(Button.right)
                mouse.release(Button.right)
                cv2.putText(frame, 'Right Click', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            elif fingers == 0:
                pyautogui.screenshot().save(f'myscreenshot_{random.randint(1,1000)}.png')
                cv2.putText(frame, 'Screenshot', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            # Scroll removed as requested
            
            cv2.drawContours(frame, [max_contour], -1, (0, 255, 0), 3)
            hull = cv2.convexHull(max_contour)
            cv2.polylines(frame, [hull], True, (255, 0, 0), 2)
    
    cv2.imshow('Working Hand Gesture Mouse', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
