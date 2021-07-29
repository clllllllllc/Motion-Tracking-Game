import time

import cv2

import HandTrackingModule as htm

p_time = 0
c_time = 0
cap = cv2.VideoCapture(0)
detector = htm.HandDetector()
while True:
    success, img = cap.read()
    img = detector.find_hands(img)
    lm_list = detector.find_position(img, draw=True)

    if len(lm_list) != 0:
        minimum = 10000
        holder = 0
        for i, lv in enumerate(lm_list):
            if lv[-1] < minimum:
                maximum = lv[-1]
                holder = i
        print(lm_list[holder])
        if holder == 8:
            print("you are pointing at me with your index finger")

    c_time = time.time()
    fps = 1 / (c_time - p_time)
    p_time = c_time

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_ITALIC, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
