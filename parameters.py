import math
import pygame
import cv2
import numpy as np


# color parameters
RED = (255, 0, 0)
BLUE = (0, 0, 255)

DEG2RAD = math.pi/180
RAD2DEG = 180/math.pi

FPS = 120
IMG_SIZE = (640, 480)
DRONE_POS = (IMG_SIZE[0]//2, 480)
SCREEN_SIZE = (800, 480)


class ENV:
    REAL = 0
    SIMULATION = 1
    DEBUG = 2
    status = SIMULATION


class RUN:
    STOP = False
    START = True


class MODE:
    EMERGENCY = 0
    TAKEOFF = 1
    LAND = 2
    FLIGHT = 3


class run_status:
    value = RUN.STOP
