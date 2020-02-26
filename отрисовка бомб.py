import pygame, os, random
import sys
import random
import copy


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

class Bomb(pygame.sprite.Sprite):
   # board = Board()
    def __init__(self, screen, width, height, x, y):
        super().__init__(screen, width, height)
        self.frames = []
        self.cut_sheet(screen, width, height)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)


    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, screen.get_width() // columns,
                                screen.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(screen.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))


    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
