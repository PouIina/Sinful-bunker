import pygame as pg

class Bed:
    def __init__(self, rect):
        self.rect = pg.Rect(rect)  # Используем переданный прямоугольник
        self.has_beads = True  # Кровать изначально имеет бусы
        self.interaction_count = 0  # Счетчик взаимодействий
        self.font = pg.font.Font(None, 30) # Шрифт для текста
        self.message = None  # Текстовое сообщение
        self.message_rect = None  # Прямоугольник для текста

    # В bed.py
    def interact(self):
        """Обрабатывает взаимодействие с кроватью."""
        self.interaction_count += 1
        if self.interaction_count == 1:
            self.message = self.font.render("Под кроватью бусы. Интересно, откуда.", True, (255, 255, 255))
        elif self.interaction_count >1:
            self.message = self.font.render("Это старая кровать...", True, (255, 255, 255))
        else:
            self.message = None
            self.message_rect = None

    def take_beads(self):
        """Возвращает бусы, если они есть, и устанавливает флаг, что их больше нет."""
        if self.has_beads:
            self.has_beads = False
            return "beads"  # Уникальный идентификатор бус
        else:
            return None