import cv2
import numpy as np
import pygame

from HandTracking import HandTrackingModule as htm

pygame.init()
detector = htm.HandDetector()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Game")

x = 200
y = 200
width = 40
height = 60
vel = 15

p_time = 0
c_time = 0
cap = cv2.VideoCapture(0)

run = True

while run:
    success, img = cap.read()
    img = detector.find_hands(img)
    lm_list = detector.find_position(img, draw=True, raw=True)
    if lm_list:
        velocity_vector_start = np.array([lm_list[0][1], lm_list[0][2]])
        velocity_vector_end = np.array([lm_list[12][1], lm_list[12][2]])

        # h, w, c = img.shape
        # cx, cy = int(lm_list[4][1] * w), int(lm_list[4][2] * h)
        # cx2, cy2 = int(lm_list[8][1] * w), int(lm_list[8][2] * h)
        # cv2.circle(img, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
        # cv2.circle(img, (cx2, cy2), 25, (255, 0, 255), cv2.FILLED)

        delta_x = velocity_vector_end[0] - velocity_vector_start[0]
        delta_y = velocity_vector_end[1] - velocity_vector_start[1]

        x += -vel * delta_x
        y += vel * delta_y

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x > vel:
        x -= vel
    if keys[pygame.K_RIGHT] and x < SCREEN_WIDTH - width - vel:
        x += vel
    if keys[pygame.K_UP]:
        y -= vel
    if keys[pygame.K_DOWN]:
        y += vel

    if x < 0:
        x += 15
    elif x > SCREEN_WIDTH - width:
        x -= 15
    if y < 0:
        y += 15
    elif y > SCREEN_HEIGHT - height:
        y -= 15

    win.fill((0, 0, 0))

    pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
    pygame.display.update()

    # cv2.imshow("Image", img)
    # cv2.waitKey(1)

pygame.quit()
