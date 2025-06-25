# cupboard.py
import pygame as pg

class Cupboard:
    def __init__(self, rect):
        self.rect = pg.Rect(rect)
        self.has_ring = True  # Изначально в шкафу есть кольцо
        self.font = pg.font.Font(None, 30)  # Шрифт для текста
        self.interaction_count = 0
        self.message = None

    def interact(self, font):
        """Обрабатывает взаимодействие со шкафом."""
        self.interaction_count += 1
        if self.interaction_count == 1:
            self.message = "Шкаф. Стоп, похоже здесь лежит кольцо."
        else:
            self.message = "Внутри только пыльная одежда."

    def take_ring(self):
        """Возвращает кольцо, если оно есть."""
        if self.has_ring:
            self.has_ring = False
            return "redring"
        else:
            return None