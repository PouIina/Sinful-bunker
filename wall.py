import pygame as pg


class Wall:
    def __init__(self, x1, y1, x2, y2):
        self.original_coords = (x1, y1, x2, y2)
        self.scaled_coords = (x1, y1, x2, y2)
        self.rect = pg.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        self.color = (255, 0, 0, 0)
        self.surface = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA)
        pg.draw.rect(self.surface, self.color, (0, 0, self.rect.width, self.rect.height))

    def update_scale(self, scale_factor):
        x1, y1, x2, y2 = self.original_coords
        self.scaled_coords = (
            x1 * scale_factor,
            y1 * scale_factor,
            x2 * scale_factor,
            y2 * scale_factor
        )
        x1, y1, x2, y2 = self.scaled_coords
        self.rect.x = min(x1, x2)
        self.rect.y = min(y1, y2)
        self.rect.width = abs(x2 - x1)
        self.rect.height = abs(y2 - y1)
        self.surface = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA)
        pg.draw.rect(self.surface, self.color, (0, 0, self.rect.width, self.rect.height))

    def apply_offset(self, offset_x, offset_y):
        self.rect.x += offset_x
        self.rect.y += offset_y

    def draw(self, surface):
        surface.blit(self.surface, self.rect)