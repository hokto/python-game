import pygame
from pygame.locals import *

pygame.init()
pygame.display.set_mode((640,400))

while True:
    if pygame.event.peek(KEYDOWN):
        break
pygame.quit()