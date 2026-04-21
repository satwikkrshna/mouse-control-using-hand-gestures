import cv2
import numpy as np
import pyautogui
from pynput.mouse import Button, Controller
import math

mouse = Controller()
pyautogui.FAILSAFE = False
screen_width, screen_height = pyautogui.size()

# HSV skin color range (narrower for better accuracy)
lower_skin = np.array([0, 20, 70])
upper_skin = np.array([20, 120, 255])

def count_fingers(contour):
    hull = cv2.convexHull(contour, returnPoints=False)
    defects = cv2.convexityDefects(contour, hull)
    count_defects = 0
    if defects is not None:
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(contour[s][0])
            end = tuple(contour[e][0])
            far = tuple(contour[f][0])
            a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
            angle = math.degrees(math.acos((b**2 + c**2 - a**2) / (2*b*c)))
            if angle <= 85 and d > 10000:  # stricter angle, depth filter
                count_defects += 1
    return count_defects + 1

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    # ROI lower frame for hand (set upper to 0)
    mask[:int(frame.shape[0]*0.3), :] = 0
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5,5), np.uint8))
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        hand_contours = [c for c in contours if 20000 < cv2.contourArea(c) < 60000]
        if hand_contours:
            max_contour = max(hand_contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(max_contour)
            aspect = float(w)/h
            if 0.6 < aspect < 1.2:  # Hand shape
                M = cv2.moments(max_contour)
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)  # Palm center dot
                smooth_x = 0.7 * smooth_x + 0.3 * cx if 'smooth_x' in globals() else cx
                smooth_y = 0.7 * smooth_y + 0.3 * cy if 'smooth_y' in globals() else cy
                # smooth_x saved
                globals()['smooth_y'] = smooth_y
                pyautogui.moveTo(int(smooth_x * screen_width / frame.shape[1]), int(smooth_y * screen_height / frame.shape[0] * 0.8))
            
            fingers = count_fingers(max_contour)
            cv2.putText(frame, f'Fingers: {fingers}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            import time
            now = time.time()
            if fingers == 1 and (not 'left' in globals() or now - globals().get('last_left', 0) > 0.5):
                globals()['last_left'] = now
                mouse.press(Button.left)
                mouse.release(Button.left)
                cv2.putText(frame, 'Left Click!', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            elif fingers == 2 and (not 'right' in globals() or now - globals().get('last_right', 0) > 0.5):
                globals()['last_right'] = now
                mouse.press(Button.right)
                mouse.release(Button.right)
                cv2.putText(frame, 'Right Click!', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            elif fingers == 0:
                import random
                pyautogui.screenshot().save(f'screenshot_{random.randint(1,1000)}.png')
                cv2.putText(frame, 'Screenshot!', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            elif fingers >= 3:
                pyautogui.scroll(3 if fingers >4 else -3)
                cv2.putText(frame, 'Scroll!', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            # Draw hull and defects dots
            hull = cv2.convexHull(max_contour)
            cv2.drawContours(frame, [max_contour], -1, (0, 255, 0), 3)
            cv2.polylines(frame, [hull], True, (255, 0, 0), 2)  # Hull lines
            hull_pts = cv2.convexHull(max_contour, returnPoints=True)
            cv2.drawContours(frame, [hull_pts], -1, (0, 255, 255), 2, cv2.LINE_AA)  # Hull points dots
            defects = cv2.convexityDefects(max_contour, cv2.convexHull(max_contour, returnPoints=False))
            if defects is not None:
                for i in range(defects.shape[0]):
                    s, e, f, d = defects[i, 0]
                    cv2.circle(frame, tuple(max_contour[f][0]), 8, (0, 0, 255), -1)  # Defect dots red
            
    cv2.imshow('OpenCV Hand Gesture Mouse', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

