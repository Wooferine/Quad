"""
Documentation

Quad by Calvin
{git repos}

{ - - -<description>- - - }
Option page to change game settings
Currently available setting -> 
Sound: Change the volume of music and sound effect
Assistance: Display the key binding

<instruction>
Just drag and drop the text into the box to access the settings
"""

import pygame
from .utility import absolute_path, IoU, Slider
from os import path
from .fonts_description import *
from pygamepopup.components import TextElement
import pygamepopup
import math
from typing import Dict
from .consts import OPTION, RETURN
import random
from .assistance import Assistance

class Option():
    def __init__(self, screen, gameState) -> None:
        self.screen: pygame.Surface = screen
        self.music = pygame.mixer.Sound("quad/sound_fx/bgm.mp3")
        self.music.play(-1)
        self.assistance = Assistance().create_image()
        self.currentState = gameState
        self.image: Dict[str, Union[pygame.Surface, Dict[str, Union[pygame.Surface, Dict[str, pygame.Surface]]]]] = {
            "gear": pygame.transform.scale(pygame.image.load(
                absolute_path(
                    path.join(
                        "assets/background-elements/gear.png"
                        )
                    )
                ).convert_alpha(), (300, 300)),
            "space": pygame.transform.scale(pygame.image.load(
                absolute_path(
                    path.join(
                        "assets/background-elements/space.png"
                        )
                    )
                ).convert_alpha(), (250, 200)),
            "slider": {
                "button": pygame.transform.scale(pygame.image.load(
                    absolute_path(
                        path.join(
                            "assets/ui-element/button.png"
                            )
                        )
                    ).convert_alpha(), (44, 44)),
                "container": pygame.transform.smoothscale(pygame.image.load(
                    absolute_path(
                        path.join(
                            "assets/ui-element/container.png"
                            )
                        )
                    ).convert_alpha(), (461, 44))
                }
            }
        self.font: Dict[str, pygame.Font] = {
            "font_option": pygame.font.Font(
                fonts_list["font_option"]["path"], 
                fonts_list["font_option"]["size"]),
        }
        self.text: Dict[str, Dict[str: Union(pygame.Surface, pygame.Rect)]] = {}
        self.space:pygame.rect = pygame.Rect(250, 150, 250, 200)
        self.occupy:bool = False
        self.current_value: int = -1
        self.slider = Slider(self.image["slider"], (100, 350), volume=100.0)

    def run(self):
        for i, x in enumerate(OPTION):
            tmp = self.font["font_option"].render(x, True, (0, 0, 0))
            tmp_rect = tmp.get_rect(topleft = (random.randint(500, 700 - 100), random.randint(100, 300)))
            self.text[f"{i}"] = {
                "surface": tmp,
                "rect": tmp_rect
            }
        active_text:int = None
        #Initialize loop
        while True:

            # Handle pygame events
            events = pygame.event.get()
            for event in events:

                # Mouse onclick event
                if (event.type == pygame.MOUSEBUTTONDOWN):
                    if event.button == 1:
                        for i, key in enumerate(self.text):
                            if self.text[key]["rect"].collidepoint(pygame.mouse.get_pos()):
                                active_text = i
                                
                # Mouse onrelease event 
                # Note: Set active_text != None to avoid error when pointing blank   
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if active_text is not None and self.occupy is False and iou > 0.3:
                            self.text[str(active_text)]["rect"].center = self.space.center
                            self.occupy = True
                            self.current_value = active_text
                        else:
                            self.occupy = False
                        active_text = None  
                
                # Mouse motion event
                if active_text is not None and event.type.__eq__(pygame.MOUSEMOTION):
                    self.text[str(active_text)]["rect"].move_ip(event.rel)
                    iou = IoU(self.space, self.text[str(active_text)]["rect"])

                # Return to main menu
                if pygame.key.get_pressed()[RETURN]:
                    
                    pygame.mouse.set_visible(True)
                    self.current_value = -1
                    self.occupy = False
                    self.currentState.gameState = "Menu"
                    self.currentState.run()

                if event.type == pygame.QUIT:
                    pygame.quit()
      
            self.screen.fill((255, 255, 255))

            self.screen.blit(self.font["font_option"].render("Settings", True, (0, 0, 0)), (300, 50))
            # Calculate relative angle
            y = pygame.mouse.get_pos()[1] - 100 
            x = pygame.mouse.get_pos()[0] - 100
            angle = -math.atan2(y, x) / math.pi * 180

            # gear rotation
            i = pygame.transform.rotate(self.image["gear"], angle)
            self.screen.blit(i, i.get_rect(center=(100, 100)))

            # Grey area
            self.screen.blit(self.image["space"], self.space.topleft)

            # Display text
            for _, key in enumerate(self.text):
                self.screen.blit(self.text[key]["surface"], self.text[key]["rect"].topleft)

            match self.current_value:
                case 0: # Sound
                    self.slider.draw(self.screen)
                    self.music.set_volume(self.slider.volume/100)
                    if event.type == pygame.MOUSEBUTTONDOWN and self.slider.button['rect'].collidepoint(pygame.mouse.get_pos()):
                        self.slider.onhold = True

                    if event.type.__eq__(pygame.MOUSEMOTION) and self.slider.onhold:
                        self.slider.update(pygame.mouse.get_pos()[0])

                    if event.type.__eq__(pygame.MOUSEBUTTONUP):
                        self.slider.onhold = False
                
                case 1: # Assistance
                    self.screen.blit(self.assistance, (100, 320))
            pygame.display.update()
