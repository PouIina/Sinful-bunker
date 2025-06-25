import pygame as pg
from wall import Wall
from cutscene import Cutscene
from exit_zone import ExitTrigger
level_objects = {"left_wall": (1, 1, 7, 256),
                 "top_wall": (1, 1, 320, 8),
                 "bottom_wall_left": (1, 247, 62, 256),
                 "exit_bottom": (63, 255, 114, 256),
                 "bottom_right": (144, 246, 320, 255),
                 "right_wall_bottom": (310, 192, 320, 256),
                 "exit_final": (319, 113, 320, 190),
                 "right_wall_top": (312, 0, 320, 112),
                 "safe": (266, 192, 308, 245),
                 "boxes": (10, 11, 42, 34),
                 "radio": (45, 10, 81, 22),
                 "medkit": (301, 87, 309, 106),
                 "boxes_bottom": (186, 224, 208, 245),
                 "boxes_bottom_2": (148, 230, 180, 245),
                 }


class Level3:
    def __init__(self, screen_width, screen_height):
        # Инициализация аудио
        pg.mixer.init()
        self.font = pg.font.Font(None, 30)
        pg.mixer.music.load('assets/DyingLight.mp3')  # Ваш файл музыки
        pg.mixer.music.play(-1)  # Зацикливание музыки

        # Загрузка и масштабирование фона
        self.original_image = pg.image.load("assets/третья/ТРЕТЬЯ КОМНАТА.png").convert_alpha()
        self.scale_factor = 1.5  # Можете изменить под свои нужды
        self.scaled_image = self.original_image
        self.rect = self.scaled_image.get_rect()
        self.screen_rect = pg.Rect(0, 0, screen_width, screen_height)

        self.cutscene_phrases = [
            "И вот ты здесь.",
            "Задумался о чём-нибудь?",
            "Что насчёт гордыни?",
            "Зная тебя, ты никогда не пойдёшь на это...",
            "Но",
            "Ты можешь попросить помощи. Если захочешь...",
            "Подойди к радио.",
        ]
        self.cutscene = Cutscene(self.cutscene_phrases, self.font, screen_width, screen_height,
                                 (255, 255, 255))  # Белый цвет
        self.show_cutscene = True  # Начинаем с показа катсцены

        self.walls = [Wall(*coords) for coords in level_objects.values()]
        self._setup_level()

        self.radio_message = None
        self.radio_message_rect = None
        self.show_radio_message = False
        self.radio_message_timer = 0
        self.has_read_radio = False

        self.radio_cutscene_phrases = [
            "Неужели?.",
            "Ладно. Поверю тебе.",
            "Дверь открыта.",
        ]

        self.radio_cutscene = Cutscene(self.radio_cutscene_phrases, self.font, screen_width, screen_height,(255, 255, 255))
        self.show_radio_cutscene = False

        self.final_exit_trigger = ExitTrigger(315 * self.scale_factor + self.rect.x, 113 * self.scale_factor + self.rect.y, 1 * self.scale_factor, 77 * self.scale_factor)
    def _setup_level(self):
        """Настройка уровня после создания"""
        # Масштабирование фона
        new_size = (
            int(self.original_image.get_width() * self.scale_factor),
            int(self.original_image.get_height() * self.scale_factor)
        )
        self.scaled_image = pg.transform.scale(self.original_image, new_size)
        self.rect = self.scaled_image.get_rect()

        # Масштабирование стен
        for wall in self.walls:
            wall.update_scale(self.scale_factor)

        # Центрирование уровня и смещение стен
        self.rect.center = self.screen_rect.center
        offset_x = self.rect.x
        offset_y = self.rect.y

        for wall in self.walls:
            wall.apply_offset(offset_x, offset_y)

    def is_player_near_radio(self, player_rect):
        """Проверяет, находится ли игрок рядом с радио."""
        x = level_objects["radio"][0] * self.scale_factor
        y = level_objects["radio"][1] * self.scale_factor
        width = (level_objects["radio"][2] - level_objects["radio"][0]) * self.scale_factor
        height = (level_objects["radio"][3] - level_objects["radio"][1]) * self.scale_factor
        radio_rect = pg.Rect(x + self.rect.x, y + self.rect.y, width, height)  # Создаем прямоугольник с учетом смещения

        # Вычисляем центр прямоугольника
        radio_center_x = radio_rect.centerx
        radio_center_y = radio_rect.centery

        # Вычисляем расстояние между игроком и центром прямоугольника
        distance = ((player_rect.centerx - radio_center_x) ** 2 + (player_rect.centery - radio_center_y) ** 2) ** 0.5

        interaction_radius = 50  # Радиус взаимодействия, может быть изменен
        return distance < interaction_radius

    def interact_with_radio(self):
        """Запускает катсцену при взаимодействии с радио."""
        if not self.has_read_radio:
            self.show_radio_cutscene = True
            self.has_read_radio = True
        else:
            self.show_radio_cutscene = False

    def update(self, player):
        if self.show_cutscene:
            self.cutscene.update()
            if self.cutscene.done:
                self.show_cutscene = False
            return

        if self.show_radio_cutscene:
            self.radio_cutscene.update()
            if self.radio_cutscene.done:
                self.show_radio_cutscene = False
            return
        if self.has_read_radio:
            self.final_exit_trigger.activate()

        for wall in self.walls:
            if player.rect.colliderect(wall.rect):
                return True
        return False

    def draw(self, surface, hero):
        surface.blit(self.scaled_image, self.rect)
        # Если нужно отображать стены (для отладки)
        for wall in self.walls:
            wall.draw(surface)

        if self.show_cutscene:
            self.cutscene.draw(surface)
        if self.show_radio_cutscene:
            self.radio_cutscene.draw(surface)

    def stop_music(self):
        pg.mixer.music.stop()