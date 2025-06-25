import pygame as pg
class Box1(pg.sprite.Sprite):
    def __init__(self, rect, has_pizza=True):
        super().__init__()
        self.rect = rect
        self.has_pizza = has_pizza
        self.message = None

    def interact(self, font, inventory):
        """Действия при взаимодействии."""
        if self.has_pizza:
            self.message = font.render("Пицца?! О ужас! Она с плесенью!", True, (255, 255, 255))
            inventory.add_item("pizza")
            self.has_pizza = False
        else:
            self.message = font.render("Пыльная коробка.", True, (255, 255, 255))