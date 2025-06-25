import pygame as pg

class Closet(pg.sprite.Sprite):
    def __init__(self, rect, has_cutters=True):
        super().__init__()
        self.rect = rect
        self.has_cutters = has_cutters
        self.message = None

    def interact(self, font, inventory):
        """Действия при взаимодействии."""
        if self.has_cutters:
            self.message = font.render("Здесь топор.", True, (255, 255, 255))
            inventory.add_item("cutters")
            self.has_cutters = False
        else:
            self.message = font.render("В шкафу только комплект защитной одежды.", True, (255, 255, 255))