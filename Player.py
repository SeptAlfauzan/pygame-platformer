import pygame
from dataclasses import dataclass


@dataclass
class Player:
    sprite = None
    position: list
    movement: list
    velocity: float

    def __init__(self):
        self.coll_rect = None;
        self.sprite = pygame.image.load('Assets/Sprites/Adventurer-1.5/Individual Sprites/adventurer-idle-00.png')
        self.position = [0, 0]
        self.movement = [0, 0]
        self.velocity = 2

        self.coll_rect = pygame.Rect(self.position[0], self.position[1], self.sprite.get_width() - 30 #subtract with 30, so the collision box's width of player can move 30px to left (so it fit the pixel)
        , self.sprite.get_height() - 5#subtract with 5, so the collision box's height of player can move 5px to top (so it fit the pixel)
        )
