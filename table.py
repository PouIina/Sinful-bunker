import pygame as pg

class Table:
    def __init__(self, rect):
        self.rect = pg.Rect(rect)
        self.has_pasport = True  # Изначально в аптечке есть паспорт
        self.font = pg.font.Font(None, 30)  # Шрифт для текста
        self.interaction_count = 0
        self.message = None

    def interact(self, font):
        """Обрабатывает взаимодействие с аптечкой."""
        self.interaction_count += 1
        if self.interaction_count == 1:
            self.message = "Здесь чей-то паспорт. Жутко."
        else:
            self.message = "Аптечка. На удивление, пустая."

    def take_pasport(self):
        """Возвращает паспорт, если он есть."""
        if self.has_pasport:
            self.has_pasport = False
            return "pasport"
        else:
            return None