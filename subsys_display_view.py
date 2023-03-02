import pygame
import numpy as np
from parameters import RED, IMG_SIZE, SCREEN_SIZE


class Display:
    # Parameters
    SCREEN = None

    LEFT_MARGIN = 5
    TOP_MARGIN = 0
    INTER_LINE = 20

    FONT_PANEL_INFO = None

    # global Variables
    pos_img_in_screen = 0
    current_line = TOP_MARGIN
    log_dict = {}

    # signals

    # methods

    @classmethod
    def _log(cls, title, value):
        """ We use the title argument as key in dictionary to save the position of the log in screen"""
        next_line = cls.current_line + cls.INTER_LINE
        position = (cls.LEFT_MARGIN, next_line)
        if title in cls.log_dict:
            cls.log_dict[title]['value'] = value
        else:
            next_line = cls.current_line + cls.INTER_LINE
            position = (cls.LEFT_MARGIN, next_line)
            cls.log_dict[title] = {"pos": position, 'value': value}
            cls.current_line = next_line

    @classmethod
    def _update_log(cls):
        for title, item in cls.log_dict.items():
            text = f"{title} {item['value']}"
            panel_info = cls.FONT_PANEL_INFO.render(text, True, RED)
            cls.SCREEN.blit(panel_info, item['pos'])

    @classmethod
    def setup(cls):
        # Init pygame
        pygame.init()
        pygame.font.init()  # The font
        cls.FONT_PANEL_INFO = pygame.font.Font('freesansbold.ttf', 18)

        # create pygame screen
        shift_left = SCREEN_SIZE[0] - IMG_SIZE[0]
        cls.pos_img_in_screen = (shift_left, 0)
        cls.SCREEN = pygame.display.set_mode(SCREEN_SIZE)

    @classmethod
    def stop(cls):
        pass

    @classmethod
    def run(cls, frame, **karg):

        cls.SCREEN.fill([0, 0, 0])

        # cls._log("Battery:", f"{DRONE_STATUS.battery}%")
        for key in karg:
            cls._log(f"{key}: ", f"{karg[key]}")

        frame = np.rot90(frame)
        frame = np.flipud(frame)
        frame = pygame.surfarray.make_surface(frame)

        cls._update_log()
        cls.SCREEN.blit(frame, cls.pos_img_in_screen)

        pygame.display.update()
