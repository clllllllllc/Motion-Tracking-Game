import random
import time

import cv2
import numpy as np
import pygame

from HandTracking import HandTrackingModule as htm


class Rock:

    def __init__(self, width, height, x, y, vel):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.xs = vel[0] - x
        self.ys = vel[1] - y
        self.speed = vel[2]

    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 255), (self.x, self.y, self.width, self.height))

    def movement(self):
        self.x += self.xs / self.speed
        self.y += self.ys / self.speed


def gen_pos(min, max, bounds):
    def_x = random.choice([0, 1])
    if def_x:
        return random.randint(min - bounds, min)
    else:
        return random.randint(max, max + bounds)


def main():
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

    # p_time = 0
    # c_time = 0
    key = [True if input() == "1" else False]

    if not key[0]:
        cap = cv2.VideoCapture(0)

    run = True
    rocks = []

    time.sleep(1)
    while run:

        if not key[0]:
            success, img = cap.read()
            img = detector.find_hands(img)
            detector.find_hands(img, draw=True)
            lm_list = detector.find_position(img, draw=True, raw=True)
            if lm_list:
                velocity_vector_start = np.array([lm_list[0][1], lm_list[0][2]])
                velocity_vector_end = np.array([lm_list[12][1], lm_list[12][2]])

                h, w, c = img.shape
                cx, cy = int(lm_list[0][1] * w), int(lm_list[0][2] * h)
                cx2, cy2 = int(lm_list[12][1] * w), int(lm_list[12][2] * h)
                cv2.circle(img, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (cx2, cy2), 25, (255, 0, 255), cv2.FILLED)

                delta_x = velocity_vector_end[0] - velocity_vector_start[0]
                delta_y = velocity_vector_end[1] - velocity_vector_start[1]

                x += -vel * delta_x
                y += vel * delta_y

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

        if x < 0:
            x += 15
        elif x > SCREEN_WIDTH - width:
            x -= 15
        if y < 0:
            y += 15
        elif y > SCREEN_HEIGHT - height:
            y -= 15

        win.fill((0, 0, 0))

        if random.choice([i for i in range(30)]) == 6:
            pos_x = gen_pos(0, 500, 50)
            pos_y = gen_pos(0, 500, 50)
            rocks.append(Rock(50.0, 50.0, pos_x, pos_y, [x, y, 30]))
        if rocks:
            for i, rock in enumerate(rocks):
                if rock.x < -100 or rock.x > 600 or rock.y < -100 or rock.y > 600:
                    rocks.pop(i)
                    continue
                if rock.x < x < rock.x + 50 and rock.y < y < rock.y + 50:
                    run = False
                if rock.x < x + 40 < rock.x + 50 and rock.y < y + 60 < rock.y + 60:
                    run = False
                rock.movement()
                rock.draw(win)

        pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
        pygame.display.update()

        pygame.time.delay(20)

        # cv2.imshow("Image", img)
        # cv2.waitKey(1)

    pygame.quit()


if __name__ == "__main__":
    main()
