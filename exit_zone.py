import pygame as pg

class ExitTrigger(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pg.Surface([width, height], pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.active = False

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def is_colliding(self, player_rect):
        if self.active:
            return self.rect.colliderect(player_rect)
        return False