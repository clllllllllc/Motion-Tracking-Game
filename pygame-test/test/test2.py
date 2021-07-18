import cv2
import numpy as np
import pygame

from HandTracking import HandTrackingModule as htm

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Game")

x = 200
y = 200
width = 40
height = 60
vel = 5

p_time = 0
c_time = 0

is_jump = False
jump_count = 10

run = True

while run:
    pygame.time.delay(20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x > vel:
        x -= vel
    if keys[pygame.K_RIGHT] and x < SCREEN_WIDTH - width - vel:
        x += vel
    if not is_jump:
        if keys[pygame.K_UP] and y > vel:
            y -= vel
        if keys[pygame.K_DOWN] and y < SCREEN_HEIGHT - height - vel:
            y += vel
        if keys[pygame.K_SPACE]:
            is_jump = True
    else:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            y -= neg * jump_count ** 2 / 2
            jump_count -= 1
        else:
            is_jump = False
            jump_count = 10


    win.fill((0, 0, 0))

    pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
    pygame.display.update()

pygame.quit()
