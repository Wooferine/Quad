"""
Documentation

Quad by Calvin
{git repos}

{ - - -<description>- - - }
Main file to kick start the game
"""
import quad
import torch
from quad.point import Point
import pygame
import screeninfo
import platform
import logging
from quad.option import Option
from quad.fonts_description import *
from quad.consts import *
from quad.menu import Menu
import sys

# Temp class and variable

class GameState():
    def __init__(self) -> None:
        self._gameState:str = "Menu"
        self.stateDict:Dict = {}

    def __add__(self, value:Dict[str, object]):
        """
        Assign value to object attributes
        :value: 
        """
        # Magic method for operator +
        self.stateDict = value

    def run(self):
        while True:
            self.stateDict[self._gameState].run()

    @property
    def gameState(self):
        return self._gameState
    
    @gameState.setter
    def gameState(self, value):
        self._gameState = value

class Quit():
    def __init__(self) -> None:
        pass

    def run(self):
        pygame.quit()
        sys.exit()

class Game():
    def __init__(self) -> None:
        """
        Main class to initialize the game
        """
        pygame.init()
        pygame.display.set_caption("Quad")
        MONITOR = screeninfo.get_monitors()[0]  # Monitor info for screen reolution feature
        self.WIDTH, self.HEIGHT = MONITOR.width, MONITOR.height
        self.screen = pygame.display.set_mode((800, 700))
        self.gameState = GameState()
        self.stateDict = {
            "Menu": Menu(self.screen, self.gameState),
            "Start": Point(self.screen, self.gameState),
            "Option": Option(self.screen, self.gameState),
            "Quit": Quit()
        }
        self.gameState + self.stateDict # Just for fun to confuse other
        


if __name__ == "__main__":
    print(f"Hello from {quad.__name__} ({quad.__doc__}) using {torch.__name__} {torch.__version__}")

    if platform.system() == "Windows":
        from ctypes import windll

        try:
            windll.user32.SetProcessDPIAware()
        except Exception as e:
            logger = logging.getLogger()
            logger.warning(e)
            pass
        
    Game().gameState.run()

        


    