# cutscene.py
import pygame as pg

class Cutscene:
    def __init__(self, phrases, font, screen_width, screen_height, text_color):
        self.phrases = phrases
        self.font = font
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.text_color = text_color
        self.current_index = 0

        self.text_surface = font.render(self.phrases[self.current_index], True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
        self.done = False

    def draw(self, surface):
        overlay = pg.Surface((self.screen_width, self.screen_height), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

        surface.blit(self.text_surface, self.text_rect)

    def update(self):
        pass

    def next_phrase(self):
        if self.current_index < len(self.phrases) - 1:
            self.current_index += 1

            self.text_surface = self.font.render(self.phrases[self.current_index], True, self.text_color)
            self.text_rect = self.text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        else:
            self.done = True