"""
Documentation

Quad by Calvin
{git repos}

{ - - -<description>- - - }
Create assistance object and generate info panel pygame image type
"""


import pygame
from typing import Dict
from .consts import FRAME_2_HEIGHT, FRAME_2_WIDTH, KEY_WIDTH, KEY_HEIGHT, BLACK, KEY_DOWN_DESCRIPTION, KEY_ESC_DESCRIPTION, KEY_RIGHT_DESCRIPTION, KEY_LEFT_DESCRIPTION, KEY_UP_DESCRIPTION


class Assistance():
    def __init__(self) -> None:
        """
        Display default key binding

        """
        pygame.init()

        # Create alternative when custom font not working
        try:
            from .fonts_description import fonts_list
            self.font: Dict[str, pygame.Font] = {
                "font_description": pygame.font.Font(
                    fonts_list["font_name"]["path"], 
                    fonts_list["font_name"]["size"]),
            }
        except ImportError:
            self.font: Dict[str, pygame.Font] = {
                "font_description": pygame.font.SysFont("arial", 30),
            }

        self.image: Dict[str, pygame.Surface] = {
            "frame": pygame.transform.scale(
                pygame.image.load("quad/assets/background-elements/frame_2.png").convert_alpha(), 
                (FRAME_2_WIDTH, FRAME_2_HEIGHT)
            ),
            "key": {
                "key_up": pygame.transform.scale(
                    pygame.image.load("quad/assets/keys/KEY_UP.png").convert_alpha(), 
                    (KEY_WIDTH, KEY_HEIGHT)
                ),
                "key_down": pygame.transform.scale(
                    pygame.image.load("quad/assets/keys/KEY_DOWN.png").convert_alpha(), 
                    (KEY_WIDTH, KEY_HEIGHT)
                ),
                "key_left": pygame.transform.scale(
                    pygame.image.load("quad/assets/keys/KEY_LEFT.png").convert_alpha(), 
                    (KEY_WIDTH, KEY_HEIGHT)
                ),
                "key_right": pygame.transform.scale(
                    pygame.image.load("quad/assets/keys/KEY_RIGHT.png").convert_alpha(), 
                    (KEY_WIDTH, KEY_HEIGHT)
                ),
                "key_esc": pygame.transform.scale(
                    pygame.image.load("quad/assets/keys/KEY_ESC.png").convert_alpha(), 
                    (KEY_WIDTH, KEY_HEIGHT)
                )
            }
        }
        self.description: Dict[str, pygame.Font] = {
            "key_up": self.font["font_description"].render(
                f": {KEY_UP_DESCRIPTION}", 
                True, 
                BLACK
            ),
            "key_down": self.font["font_description"].render(
                f": {KEY_DOWN_DESCRIPTION}", 
                True, 
                BLACK
            ),
            "key_left": self.font["font_description"].render(
                f": {KEY_LEFT_DESCRIPTION}", 
                True, 
                BLACK
            ),
            "key_right": self.font["font_description"].render(
                f": {KEY_RIGHT_DESCRIPTION}", 
                True, 
                BLACK
            ),
            "key_esc": self.font["font_description"].render(
                f": {KEY_ESC_DESCRIPTION}", 
                True, 
                BLACK
            )
        }

    def create_image(self) -> pygame.Surface:
        # Blitting key image and description through looping      
        for i, key in enumerate(self.image['key']):
            self.image["frame"].blit(self.image['key'][key], (50, 60 * (i) + 40))
            self.image["frame"].blit(self.description[key], (100, 60 * (i) + 40))

        return self.image["frame"]
