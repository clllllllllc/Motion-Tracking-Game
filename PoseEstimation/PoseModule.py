import cv2
import mediapipe as mp
import time

class PoseDetector():

    def __init__(self, mode=False, complexity=1, smooth=True, detection_con=0.5, track_con=0.5):

        self.mode = mode
        self.complexity = complexity
        self.smooth = smooth
        self.detection_con = detection_con
        self.track_con = track_con


        self.mp_draw = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(self.mode, self.complexity, self.smooth, self.detection_con, self.track_con)

        self.results = None

    def find_pose(self, img, draw=True):

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(img_rgb)
        if self.results.pose_landmarks:
            if draw:
                self.mp_draw.draw_landmarks(img, self.results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
        return img

    def find_pos(self, img, draw=False):
        lmList = []
        if self.results.pose_landmarks:
            self.mp_draw.draw_landmarks(img, self.results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
            for index, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([index, cx, cy, lm.z, lm.visibility])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)


def main():
    cap = cv2.VideoCapture('videos/test.mp4')
    p_time = 0
    detector = PoseDetector()
    while True:
        success, img = cap.read()
        detector.find_pose(img)
        detector.find_pos(img, True)
        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time

        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_ITALIC, 3, (255, 0, 255), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
