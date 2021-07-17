import HandTrackingModule as htm
import cv2
import numpy as np
import time

from PoseEstimation import PoseModule as pm

CAM_WIDTH = 640
CAM_HEIGHT = 480


def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, CAM_WIDTH)
    cap.set(4, CAM_HEIGHT)
    previous_time = 0
    detector = htm.HandDetector()
    detector2 = pm.PoseDetector()
    while True:
        success, img = cap.read()
        # detector.find_hands(img, draw=True)
        detector2.find_pose(img, draw=True)
        current_time = time.time()
        time_delta = 1 / (current_time - previous_time)
        previous_time = current_time

        cv2.putText(img, f'FPS: {str(int(time_delta))}', (20, 40), cv2.FONT_ITALIC, 1, (0, 0, 0), 1)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
