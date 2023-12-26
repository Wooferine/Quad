"""
Documentation

Quad by Calvin
{git repos}

{ - - -<description>- - - }
The main menu UI for Quad game

Start -> To initialize the main game
Option -> To change settings
Quit -> To exit the application 

Enjoy !
"""
import pygame
from .utility import Button, absolute_path
from .consts import *
from os import path
from typing import Union, Dict

class Menu():
    def __init__(self, screen, gameState) -> None:
        """
        Class to control the main menu UI elements
        :screen: Pygame surface where objects were blitted on
        :gameState: Game state manager
        """
        self.FPS: int = FPS
        self.screen: pygame.Surface = screen
        self.gameState: object = gameState
        self.background: pygame.Surface = pygame.transform.scale(
            pygame.image.load(absolute_path(
                    path.join(
                        f"assets/background-elements/Menu.png"
                        )
                    )),
            (800, 700)
            )

    def run(self):
        # Initialize loop
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    quit()
                  
            pygame.time.Clock().tick(self.FPS)
            self.screen.blit(self.background, (0, 0))

            # Create Menu interactable buttons
            btn_1 = Button(
                rect=pygame.Rect(260,200,200,90),
                callback = self.gameState,
                font="assets/fonts/Lewiscarroll.ttf",
                font_size=50,
                text="Start",
                outline=None,
                angle=10
            )

            btn_2 = Button(
                rect=pygame.Rect(268,285,200,90),
                callback = self.gameState,
                font="assets/fonts/Lewiscarroll.ttf",
                font_size=50,
                text="Option",
                outline=None,
                angle=10
            )

            btn_3 = Button(
                rect=pygame.Rect(285,375,200,90),
                callback = self.gameState,
                font="assets/fonts/Lewiscarroll.ttf",
                font_size=50,
                text="Quit",
                angle=10,
                outline=None,
            )

            sprites = pygame.sprite.Group()
            sprites.add(btn_1, btn_2, btn_3)

            # Update event
            sprites.update(events)
            sprites.draw(self.screen)
            
            pygame.display.update()