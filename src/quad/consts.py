#[RUNTIME]
FPS                         = 60
WIDTH                       = 800
HEIGHT                      = 700

#[ENVIRONMENT]
GRAVITY                     = 0.08

#[QUAD PHYSICS]
MASS                        = 1.0
THRUSTER_AMPLITUDE          = 0.04
ARM                         = 25
SECOND_MOMENT_INERTIA       = 1.0
EFFECTIVE_LENGTH            = 25.0
FORCE_MEAN                  = 0.04
FORCE_AMPLITUDE             = 0.04

#[GAMEPLAY]
PLAYER_SIZE                 = 120
PLAYER_ANIMATION_SPEED      = 0.3
PLAYER_RESPAWN              = 4
GAME_TIME                   = 100

#Option
OPTION                      = ["Sound", "Assistance"] # Expandable setting control list, future update

#[KEY CONTROL]
from pygame.locals import *
UP                          = K_UP
DOWN                        = K_DOWN
CCW                         = K_LEFT
CW                          = K_RIGHT
RETURN                      = K_ESCAPE

#[SOUND EFFECT]
BGM                         = "quad/sound_fx/bgm.mp3"
POINT                       = "quad/sound_fx/take_point_1.wav"

#[UI]
FRAME_WIDTH                 = 300
FRAME_HEIGHT                = 300
FRAME_2_WIDTH               = 560
FRAME_2_HEIGHT              = 360
KEY_WIDTH                   = 50
KEY_HEIGHT                  = 50

#[COLOR]
BLACK                       = (0, 0, 0)
WHITE                       = (255, 255, 255)

#[TEXT]
KEY_UP_DESCRIPTION          = "Accelerating the drone."
KEY_DOWN_DESCRIPTION        = "Decelerating the drone."
KEY_LEFT_DESCRIPTION        = "Rotate the drone counter-clockwise."
KEY_RIGHT_DESCRIPTION       = "Rotate the drone clockwise."
KEY_ESC_DESCRIPTION         = "Return to main menu."
