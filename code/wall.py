import numpy as np
import pygame
scaling_factor = 1

class Wall:
    def __init__(self,start,end,width=6):
        self.start = self.screen_to_position(start)
        self.end = self.screen_to_position(end)
        self.width = self.screen_to_position(width)

    def draw(self,screen):
        start = self.position_to_screen(self.start)
        end = self.position_to_screen(self.end)
        pygame.draw.line(screen, "black", (round(start[0]),round(start[1])), (round(end[0]),round(end[1])), width = round(self.position_to_screen(self.width)))

    def screen_to_position(self,vec):
        return vec * scaling_factor

    def position_to_screen(self,vec):
        return vec / scaling_factor

    def update(self, t,objects):
        pass

    @staticmethod
    def create_box(co_1, co_2, co_3, co_4):
        return[Wall(co_1,co_2),Wall(co_2,co_3),Wall(co_3,co_4),Wall(co_4,co_1)]
