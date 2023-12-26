"""
Documentation

Quad by Calvin
{git repos}

{ - - -<description>- - - }
set manual control for Human and automatic control for AI
Manual -> float (left and right Thruster)
    set pygame key pressed
    UP for amplitude addition in both thruster
    Down for amplitude deduction in both thruster
    CW for stronger right thruster and hover towards left side
    CCW for stronger left thruster and hover towards right side
"""
import pygame
from pygame.locals import *
from .consts import UP, DOWN, CCW, CW

class Player:
    def __init__(self):
        """
        Basic Drone class for inheritance purpose
        """
        self.force_mean: float = 0.04
        self.force_amplitude: float = 0.04
        self.difference_amplitude: float = 0.003
        (self.angle, self.angular_speed, self.angular_acceleration) = (0, 0, 0)
        (self.position, self.velocity, self.acceleration) = ([400, 400] ,[0, 0] ,[0, 0])
        self.target_counter: int = 0
        self.alive: bool = True
        self.respawn_timer: int = 0
        self.revive:int = 0

class Human(Player):
    def __init__(self):
        """"
        Player control with custom key binding setting class
        :name: ID for player control drone
        :alpha: Set transparency
        """
        super().__init__()
        self.name: str = "Human"
        self.alpha: int = 255
    
    def control(self):
        self.thruster_left = self.force_mean
        self.thruster_right = self.force_mean

        # Key press control
        press = pygame.key.get_pressed()

        if press[UP]:
            self.thruster_left += self.force_amplitude
            self.thruster_right += self.force_amplitude

        if press[DOWN]:
            self.thruster_left -= self.force_amplitude
            self.thruster_right -= self.force_amplitude

        if press[CCW]:
            self.thruster_left -= self.difference_amplitude

        if press[CW]:
            self.thruster_right -= self.difference_amplitude

        return self.thruster_left, self.thruster_right

# AI Class: Inherit player <Second phase>
# Future update
class NeatAi(Player):
    def __init__(self):
        """
        AI control drone and self training class
        :name: ID for AI control drone
        :alpha: Set transparency
        :radars: COllect input for neural networks
        :time: Reward system
        :point: Reward system
        """
        super().__init__()
        self.name: str = "Neat"
        self.alpha: int = 255
        self.radars: list[int] = []
        self.time: int = 0
        self.point: int = 0

    def check_radar(self, theta: float):
        l = 0
        x = 1
