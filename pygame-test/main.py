import pygame
import cv2
from HandTracking import HandTrackingModule as htm
import numpy as np

pygame.init()
detector = htm.HandDetector()

win = pygame.display.set_mode((500, 500))

pygame.display.set_caption("Game")

x = 50
y = 50
width = 40
height = 60
vel = 10

p_time = 0
c_time = 0
cap = cv2.VideoCapture(0)

run = True

while run:
    success, img = cap.read()
    img = detector.find_hands(img)
    lm_list = detector.find_position(img, draw=True, raw=True)

    velocity_vector_start = np.array([lm_list[4].x, lm_list[4].y])
    velocity_vector_end = np.array([lm_list[8].x, lm_list[8].y])

    delta_x = velocity_vector_end[0] - velocity_vector_start[0]
    delta_y = velocity_vector_end[1] - velocity_vector_start[1]

    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= vel
    if keys[pygame.K_RIGHT]:
        x += vel
    if keys[pygame.K_UP]:
        y -= vel
    if keys[pygame.K_DOWN]:
        y += vel

    x += vel * delta_x
    y += vel * delta_y

    win.fill((0, 0, 0))

    pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
    pygame.display.update()

pygame.quit()
