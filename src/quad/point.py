"""
Documentation

Quad by Calvin
{git repos}

{ - - -<description>- - - }
Control the Quadcopter using basic key arrow up, arrow down, arrow left, arrow right

custom key binding:
    Arrow Up: Accelerate
    Arrow Down: Decelerate
    Arrow Left: Rotate left
    Arrow Right: Rotate right
    ESC: Return to Main menu

<Instruction>
To make changes on game constants, refer to ./src/consts.py and modify the value according to your preferences
"""
import pygame
import random
import math
from .player import Human
from os import path
import logging
from .utility import absolute_path
from .consts import * 
from .fonts_description import *
import time

# logging control
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S"
    )  


class Point():
    def __init__(self, screen, gameState):
        """
        Main class to run the game

        :screen: Surface where objects are blitted
        :FPS: Control the game speed
        :gameState: Game state control
        :font: Font used during the game
        """
        self.screen: pygame.Surface = screen
        self.FPS = FPS
        self.pause = False
        self.currentState:object = gameState
        self.game_over = False
        self.sound: Dict[str, pygame.mixer.Sound] = {
            "point": pygame.mixer.Sound(POINT)
        }
        self.font: Dict[str, pygame.Font] = {
            "font_name": pygame.font.Font(
                fonts_list["font_name"]["path"], 
                fonts_list["font_name"]["size"]),
            "font_HUD": pygame.font.Font(
                fonts_list["font_HUD"]["path"], 
                fonts_list["font_HUD"]["size"]),
            "font_respawn": pygame.font.Font(
                fonts_list["font_respawn"]["path"], 
                fonts_list["font_respawn"]["size"]),
            "font_end": pygame.font.Font(
                fonts_list["font_end"]["path"], 
                fonts_list["font_end"]["size"]),
        }

    def run(self):
        #game
        pygame.mouse.set_visible(False)

        #Player screening
        player_size = PLAYER_SIZE
        player_animation_speed = PLAYER_ANIMATION_SPEED
        player_frame = []
        for i in range(1, 3):   # Player animation
            player = pygame.image.load(
                absolute_path(
                    path.join(
                        f"assets/objects/Quad-sprites/drone_{i}.png"
                        )
                    )
                ).convert_alpha()
            player = pygame.transform.scale(player, (player_size, player_size))
            player_frame.append(player)

        #target screening
        target_size = 50
        target_animation_speed = 0.1
        target_frame = []
        for i in range(1, 5):   # Target animation
            target = pygame.image.load(
                absolute_path(
                    path.join(
                        f"assets/objects/circle-sprites/circle-{i}.png"
                        )
                    )
                ).convert_alpha()
            target = pygame.transform.scale(target, (target_size, target_size))
            target_frame.append(target)

        #Background screening
        cloud_1 = pygame.image.load(
                absolute_path(
                    path.join(
                        f"assets/background-elements/cloud_1.png"
                        )
                    )
                ).convert_alpha()

        cloud_2 = pygame.image.load(
                absolute_path(
                    path.join(
                        f"assets/background-elements/cloud_2.png"
                        )
                    )
                ).convert_alpha()
        
        sun = pygame.image.load(
                absolute_path(
                    path.join(
                        f"assets/background-elements/sun.png"
                        )
                    )
                ).convert_alpha()
        
        background = pygame.image.load(
                absolute_path(
                    path.join(
                        f"assets/background-elements/paper.jpg"
                        )
                    )
                ).convert()
        background = pygame.transform.scale(background, (800, 800))

        cloud_1.set_alpha(255)
        (cloud_1_x, cloud_1_y, cloud_1_speed) = (100, 100, 0.5)
        cloud_1_mask = pygame.mask.from_surface(cloud_1).outline()   # Shadow
        cloud_1_mask = [(x + cloud_1_x - 10,  y + cloud_1_y + 15) for x, y in cloud_1_mask]
        

        cloud_2.set_alpha(255)
        (cloud_2_x, cloud_2_y, cloud_2_speed) = (600, 600, 0.3)
        cloud_2_mask = pygame.mask.from_surface(cloud_2).outline()  # Shadow
        cloud_2_mask = [(x + cloud_2_x - 10,  y + cloud_2_y + 15) for x, y in cloud_2_mask] 
        
       

        targets = [(random.randrange(100, 600), random.randrange(100, 600)) for i in range(100)]    # Target random spawning
        player = Human()

        # List of pre-game variables 
        step = 0
        LOG = False      # LOGGING Control
        clock = pygame.time.Clock()
        starting_time = time.time()
        self.pause = False
        player.revive = 0

        while True:
            # Game loop control
            self.screen.blit(background, (0, 0))
            self.screen.blit(sun, (600, -200))

            cloud_1_x = -200 if cloud_1_x > 800 else cloud_1_x + cloud_1_speed  # Control cloud speed and reset position 
            cloud_1_mask = [(x + cloud_1_speed, y) for x, y in cloud_1_mask] if cloud_1_mask[0][0] < 893 else [(x - 1005, y) for x, y in cloud_1_mask]  # Control shadow speed and reset position 
            pygame.draw.polygon(self.screen, (0, 0, 0, 0), cloud_1_mask)
            self.screen.blit(cloud_1, (cloud_1_x, cloud_1_y))
            
            cloud_2_x = 900 if cloud_2_x < -200 else cloud_2_x - cloud_2_speed  # Control cloud speed and reset position 
            cloud_2_mask = [(x - cloud_2_speed,  y) for x, y in cloud_2_mask] if cloud_2_mask[0][0] > -101 else [(x + 1105, y) for x, y in cloud_2_mask]  # Control cloud speed and reset position 
            pygame.draw.polygon(self.screen, (0, 0, 0, 0), cloud_2_mask)
            self.screen.blit(cloud_2, (cloud_2_x, cloud_2_y))

            step += 1

            # Displaying game info
            elapsed_time = GAME_TIME - int(time.time() - starting_time) if not self.pause else elapsed_time
            self.screen.blit(self.font["font_name"].render(f"Player: {player.target_counter}", True, (0,0,0)), (50,50))
            self.screen.blit(self.font["font_HUD"].render(f"Timer: {elapsed_time}", True, (0,0,0)), (300,50))
            
            # Player physics calculation
            if player.alive == True:

                # Reset x, y, angular acceleration each frame if no input detected
                player.acceleration[0] = 0
                player.acceleration[1] = GRAVITY
                player.angular_acceleration = 0

                # Calculate acceleration
                Thrust_L, Thrust_R = player.control()
                player.acceleration[0] += (
                    -(Thrust_L + Thrust_R) 
                    * math.sin(math.radians(player.angle)) 
                    / (MASS*3)
                    )
                player.acceleration[1] += (
                    -(Thrust_L + Thrust_R) 
                    * math.cos(math.radians(player.angle)) 
                    / MASS
                    )
                player.angular_acceleration += (
                    -(Thrust_L - Thrust_R)
                    * EFFECTIVE_LENGTH
                    / SECOND_MOMENT_INERTIA
                )

                # Calculate Velocity and position
                player.velocity = [x + player.acceleration[i] for i, x in enumerate(player.velocity)]
                player.position = [y + player.velocity[i] for i, y in enumerate(player.position)]

                # Calculate angular velocity and angle
                player.angular_speed += player.angular_acceleration
                player.angle += player.angular_speed 

                # Calculate distance between target and player
                dist = math.sqrt(
                        (player.position[0] - targets[player.target_counter][0]) ** 2
                        + (player.position[1] - targets[player.target_counter][1]) ** 2
                        )
                logging.info(f"Distance: {dist}") if LOG else None                
                
                # Earn point
                if dist < 60:
                    player.target_counter += 1
                    self.sound['point'].play()
                    # counter += 1
                elif dist > 1800:
                    player.alive = False
                    player.respawn_timer = PLAYER_RESPAWN
            
            # Player respawn condition
            else:
                player.respawn_timer -= 1 / self.FPS
                self.screen.blit(self.font["font_respawn"].render(
                    f"Respawn time: {int(player.respawn_timer)}", 
                    True, 
                    (0,0,0)),
                    (300, 400)
                    )

                if player.respawn_timer < 0:
                    self.game_over = True
                    # Reset player state
                    player.alive = True
                    player.revive += 1
                    (player.acceleration, player.velocity, player.position) = ([0, 0], [0, 0], [400, 400])
                    (player.angular_acceleration, player.angular_speed, player.angle) = (0, 0, 0)
            
            # Animation frame control
            target_image = target_frame[int((step * target_animation_speed) % len(target_frame))]
            player_image = player_frame[int((step * player_animation_speed) % len(player_frame))]

            # Player rotation
            player_copy = pygame.transform.rotate(player_image, player.angle).convert_alpha()

            # Blit target
            self.screen.blit(
                target_image, 
                target_image.get_rect(center = targets[int(player.target_counter)])
            )

            # Blit player
            self.screen.blit(
                player_copy, 
                (
                    player.position[0] - int(player_copy.get_width()/2),
                    player.position[1] - int(player_copy.get_height()/2)
                )
            )

            # Game-over
            if elapsed_time <= 0:
                self.end(player.target_counter, player.revive)

                # Reset game and player Stats
                elapsed_time = 0
                self.pause = True
                (player.acceleration, player.velocity, player.position) = ([0, 0], [0, 0], [400, 400])
                (player.angular_acceleration, player.angular_speed, player.angle) = (0, 0, 0)

            # Event control
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        LOG = not LOG
                    elif event.key == pygame.K_ESCAPE:

                        # Update note: create new UI for option.
                        # Applicable when changing "Menu" -> "New UI"
                        pygame.mouse.set_visible(True)
                        self.currentState.gameState = "Menu"
                        self.currentState.run()

            pygame.display.update()
            clock.tick(self.FPS)

    # End game condition
    def end(self, score:int, revive):
        """"
        Call when time count reach 0
        :score: Total score earn
        :revive: Number of times revived
        """

        # Stats frame
        frame = pygame.image.load(
                absolute_path(
                    path.join(
                        "assets/background-elements/frame.png"
                        )
                    )
                ).convert_alpha()
        
        # Info printing
        frame.blit(self.font["font_end"].render(
                    "Game Over", 
                    True, 
                    (0,0,0)),
                    (80, 30)
                    )
        frame.blit(self.font["font_end"].render(
                    f"Total Score: {int(score)}", 
                    True, 
                    (0,0,0)),
                    (40, 90)
                    )
        frame.blit(self.font["font_end"].render(
                    f"Total respawn: {int(revive)}", 
                    True, 
                    (0,0,0)),
                    (40, 120)
                    )
        frame.blit(self.font["font_end"].render(
                    "Press ESC to continue.", 
                    True, 
                    (0,0,0)),
                    (30, 200)
                    )
        self.screen.blit(frame, (200, 200))
