import os.path as path
import pygame
from typing import Any, Dict
def absolute_path(p: str)-> path:
    """
    Return absolute path of argument type path

    :p: Stringify path
    """
    return path.join(path.dirname(__file__), p)

def IoU(box1:pygame.Rect, box2:pygame.Rect) -> float:
    """
    General IoU calculation for pygame.Rect type data. 
    Return IoU of 2 boxes.
    Further IoU information for different type of data can refer to:
    https://pyimagesearch.com/2016/11/07/intersection-over-union-iou-for-object-detection/

    :box1, box2: Pygame rect with expected format of <rect(x, y, w, h)>

    return IoU between 0.0 and 1.0
    """

    def _area(box:pygame.Rect) -> float:
        # return area
        return box[2] * box[3]

    #intersection = (x1 + w1 - x2) * (y1 + h1 - y2)
    intersection = (box1[0] + box1[2] - box2[0]) * (box1[1] + box1[3] - box2[1]) 
    IoU = intersection / (_area(box1) + _area(box2) - intersection) # intersection / total_area - intersection
    return IoU

class Button(pygame.sprite.Sprite):
    """
    Referencing -> https://www.geeksforgeeks.org/hover-button-in-pygame/
    An interactable button

    A graphical button class can be used in a user interface.

    :rect: Pygame rect
    :callback: Event occur when interacting with button
    :font_size: Displayed font size
    :color: Displayed button color
    :color_hover: Displayed button color when cursor hovering over
    :text: String displayed on the button surface
    :outline: Color for button outline
    :angle: Rotated angle for button
    """
    def __init__(
            self, 
            rect:pygame.rect, 
            callback:Any, font:str="", 
            font_size:int=None, 
            color:tuple=None, 
            color_hover:tuple=None, 
            text:str ='', 
            outline:tuple=None, 
            angle:float=None, 
        ):

        super().__init__()
        self.text = text
        self.callback = callback
        self.rect = rect
        self.angle = angle

        # Temp size storing rect
        tmp_rect = pygame.Rect(0, 0, *rect.size)

        # Hovering effect
        self.font = pygame.font.Font(
            absolute_path(font), 
            font_size
        )

        self.hover_font = pygame.font.Font(
            absolute_path(font), 
            font_size + 20
        )
        
        self.nor = self._create_img(self.font, outline, text, tmp_rect, color)
        self.hov = self._create_img(self.hover_font, outline, text, tmp_rect, color_hover)
        self.image = self.nor
        

    def _create_img(
            self, 
            font:str, 
            outline:tuple, 
            text:str, 
            rect:pygame.rect, 
            color:pygame.color=pygame.Color('white')
        ):
        """
        Class internal used method to render image for button

        :font: Displayed font style
        :outline: Color for button outline
        :text: String to display on the button surface
        :rect: Pygame rect
        :color: Display button color

        """
        img = pygame.Surface(rect.size)
        if outline:
            img.fill(outline)
            img.fill(pygame.Color('white'), rect.inflate(-4, -3))
        else:
            img.fill(pygame.Color('white'))
        
        if text !='':
            text_surf = font.render(text, True, pygame.Color('black'))
            text_rect = text_surf.get_rect(center=rect.center)
            img.blit(text_surf, text_rect)

            # Set colorkey to remove specific color
            img.set_colorkey((255,255,255))

            # Rotate image surface
            img = pygame.transform.rotate(img, self.angle).convert_alpha() if self.angle else img.convert_alpha()

        return img
    
    def update(self, events:pygame.event):
        """
        Create event for button

        :events: Interaction with button
        """
        # Check collision
        pos = pygame.mouse.get_pos()
        hit = self.rect.collidepoint(pos)

        # Handle click event
        self.image = self.hov if hit else self.nor
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and hit:
                self.callback.gameState = self.text
                self.callback.run()

class Slider():
    def __init__(self, image: Dict[str, pygame.Surface], pos: tuple[int, int], volume:float) -> None:
        super().__init__()
        self.pos = pos
        self._volume = volume
        self.container = {
            "surface": image["container"],
            "rect": image["container"].get_rect(topleft=pos)
            }
        self.button = {
            "surface": image["button"],
            "rect": image["button"].get_rect(center=(self.pos[0]+self.container['rect'].w*(self._volume/100), self.pos[1]+25))
            }
        self.range = [self.pos[0],(self.pos[0]+self.container['rect'].w)/1.075]
        self.onhold = False
        
    def draw(self, screen):
        screen.blit(self.container['surface'], self.container['rect'])
        screen.blit(self.button['surface'], self.button['rect'])
        
    
    def update(self, x):
        self.button['rect'].centerx = x
        self.button['rect'].x = min(self.button['rect'].x, max(self.range))
        self.button['rect'].x = max(self.button['rect'].x, min(self.range))
        self.volume = self._calculate_volume()

    
    def _calculate_volume(self):
        return int(((self.button['rect'].x - self.container['rect'].x)*1.1/self.container['rect'].w)*100)

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        self._volume = value
