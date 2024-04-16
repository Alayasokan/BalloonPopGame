
# import pygame

import random
import pygame
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time

# Initialize
pygame.init()

# Create Window
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Balloon Pop Game")

# Initialize Clock for FPSf
fps = 30
clock = pygame.time.Clock()

# WebCam
cap = cv2.VideoCapture(0)
cap.set(3, 1280) #width
cap.set(4, 720) #height

# Images
imgBalloon = pygame.image.load('Resources/Images/balloon_image.png').convert_alpha()
imgBalloon = pygame.transform.smoothscale(imgBalloon, (150, 150))
rectBalloon = imgBalloon.get_rect()
rectBalloon.x, rectBalloon.y = 500, 500

# Variable
speed = 15
score = 0
startTime = time.time()
totalTime = 7

# Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

def resetBalloon():
    rectBalloon.x = random.randint(100, img.shape[1] - 100)
    rectBalloon.y = img.shape[0]+40

# Main Loops
start = True
while start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()


    # Logic
    remainingTime = int(totalTime - (time.time()-startTime))
    if remainingTime < 0:
        window.fill((255, 255, 255))

        font = pygame.font.Font('Resources/Font/BebasNeue-Regular.ttf', 50)
        textScore = font.render(f'Your Score: {score}', True, (50, 50, 255))
        textTime = font.render(f'Time Up', True, (50, 50, 255))
        window.blit(textScore, (450, 350))
        window.blit(textTime, (530, 275))
    else:
        # OpenCV
        success, img = cap.read()
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img, flipType=False)
        rectBalloon.y -= speed
        if rectBalloon.y < 0:
            resetBalloon()
            speed += 1

        if hands:
            hand = hands[0]
            lmList = hand['lmList'][8]
            x, y = lmList[:2]
            if rectBalloon.collidepoint(x, y):
                resetBalloon()
                score += 10
                speed += 1

        imgRGB = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        imgRGB = np.rot90(imgRGB)
        frame = pygame.surfarray.make_surface(imgRGB).convert()
        frame = pygame.transform.flip(frame, True, False)
        window.blit(frame, (0, 0))
        window.blit(imgBalloon, rectBalloon)
        font = pygame.font.Font('Resources/Font/BebasNeue-Regular.ttf', 50)
        textScore = font.render(f'Score: {score}', True, (50, 50, 255))
        textTime = font.render(f'Time: {remainingTime}', True, (50, 50, 255))
        window.blit(textScore, (35, 35))
        window.blit(textTime, (1100, 35))


    # Update Display/Window
    pygame.display.update()

    # Set FPS
    clock.tick(fps)