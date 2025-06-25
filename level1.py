import pygame as pg
from wall import Wall
from walls_data import create_walls
from bed import Bed
from cupboard import Cupboard
from table import Table
from cutscene import Cutscene
from safe import Safe
from exit_zone import ExitTrigger
import walls_data

class Level1:
    def __init__(self, screen_width, screen_height):
        # Инициализация аудио
        pg.mixer.init()
        pg.mixer.music.load('assets/DyingLight.mp3')
        pg.mixer.music.play(-1)  # Зацикливание музыки

        # Загрузка и масштабирование фона
        self.original_image = pg.image.load("assets/первая/ПЕРВАЯ КОМНАТА.png").convert_alpha()
        self.scale_factor = 1.5
        self.scaled_image = self.original_image
        self.rect = self.scaled_image.get_rect()
        self.screen_rect = pg.Rect(0, 0, screen_width, screen_height)

        pg.font.init()
        self.font = pg.font.Font(None, 30)



        self.walls = create_walls()
        self.bed = Bed(self.walls[9].rect)
        self.cupboard = Cupboard(self.walls[7].rect)
        self.table = Table(self.walls[8].rect)
        self.inventory_y = 700

        self.safe = Safe(self.walls[6].rect)

        # Атрибуты для сообщения от кровати
        self.bed_message = None
        self.bed_message_rect = None
        self.show_bed_message = False
        self.bed_message_timer = 0

        # Атрибуты для сообщения от шкафа
        self.cupboard_message = None
        self.cupboard_message_rect = None
        self.show_cupboard_message = False
        self.cupboard_message_timer = 0

        # Атрибуты для сообщения от стола
        self.table_message = None
        self.table_message_rect = None
        self.show_table_message = False
        self.table_message_timer = 0


        self.cutscene_phrases = [
            "Эй!",
            "Вобще-то, это мои вещи!",
            "Верни их на место, СЕЙЧАС ЖЕ!",
            "Это код от сейфа. Бери его и ПРОВАЛИВАЙ!",
        ]
        self.cutscene = Cutscene(self.cutscene_phrases, self.font, self.screen_rect.width, self.screen_rect.height, (255, 0, 0))  # Красный цвет
        self.show_cutscene = False

        self._setup_level()

        # Атрибуты для сообщения от сейфа
        self.safe_message = None
        self.safe_message_rect = None
        self.show_safe_message = False
        self.message_timer = 0

        safe_rect = self.safe.rect
        x = safe_rect.x - 100
        y = safe_rect.y + 50
        width = safe_rect.width
        height = safe_rect.height//2
        self.exit_trigger = ExitTrigger(x, y, width, height)
        self.exit_trigger.deactivate()


    def _setup_level(self):
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


    def update(self, player, inventory):
        """Обновление состояния уровня"""
        if self.show_cutscene:
            return False

        if self.show_safe_message:
            if pg.time.get_ticks() - self.message_timer > 2000:
                self.show_safe_message = False
                self.safe_message = None
                self.safe_message_rect = None

        # Таймер для сообщения кровати
        if self.show_bed_message:
            if pg.time.get_ticks() - self.bed_message_timer > 2000:
                self.show_bed_message = False
                self.bed_message = None
                self.bed_message_rect = None

        # Таймер для сообщения шкафа
        if self.show_cupboard_message:
            if pg.time.get_ticks() - self.cupboard_message_timer > 2000:
                self.show_cupboard_message = False
                self.cupboard_message = None
                self.cupboard_message_rect = None

        # Таймер для сообщения стола
        if self.show_table_message:
            if pg.time.get_ticks() - self.table_message_timer > 2000:
                self.show_table_message = False
                self.table_message = None
                self.table_message_rect = None

        if "key" in inventory.slots and not self.exit_trigger.active:
            self.exit_trigger.activate()


        return False

    def draw(self, surface, player):
        """Отрисовка уровня"""
        surface.blit(self.scaled_image, self.rect)
        for wall in self.walls:
            wall.draw(surface)

        if self.show_safe_message and self.safe_message is not None and self.safe_message_rect is not None:
            surface.blit(self.safe_message, self.safe_message_rect)


        if self.show_bed_message and self.bed_message and self.bed_message_rect:
            surface.blit(self.bed_message, self.bed_message_rect)

        if self.show_cupboard_message and self.cupboard_message and self.cupboard_message_rect:
            surface.blit(self.cupboard_message, self.cupboard_message_rect)

        if self.show_table_message and self.table_message and self.table_message_rect:
            surface.blit(self.table_message, self.table_message_rect)

        if self.show_cutscene:
            self.cutscene.draw(surface)

    def stop_music(self):
        pg.mixer.music.stop()

    def give_key_to_safe(self):
        self.safe.has_key = True

    def is_player_near_safe(self, player_rect):
        safe_rect = self.walls[6].rect
        inflated_rect = safe_rect.inflate(50, 50)
        return player_rect.colliderect(inflated_rect)

    def is_player_near_radio(self, player_rect):
        safe_rect = self.walls[10].rect
        inflated_rect = safe_rect.inflate(50, 50)
        return player_rect.colliderect(inflated_rect)

    def is_player_near_bed(self, player_rect):
        bed_rect = self.walls[9].rect
        distance = ((player_rect.centerx - bed_rect.centerx) ** 2 + (player_rect.centery - bed_rect.centery) ** 2) ** 0.5
        interaction_radius = 100
        return distance < interaction_radius

    def is_player_near_cupboard(self, player_rect):
        cupboard_rect = self.walls[7].rect
        distance = ((player_rect.centerx - cupboard_rect.centerx) ** 2 + (player_rect.centery - cupboard_rect.centery) ** 2) ** 0.5
        interaction_radius = 100  # Можно настроить
        return distance < interaction_radius

    def is_player_near_table(self, player_rect):
        table_rect = self.walls[8].rect
        distance = ((player_rect.centerx - table_rect.centerx) ** 2 + (player_rect.centery - table_rect.centery) ** 2) ** 0.5
        interaction_radius = 100
        return distance < interaction_radius


    def interact_with_safe(self, inventory):
        if self.safe.has_key:
            item = self.safe.take_key()
            if item:
                inventory.add_item(item)
                self.safe.has_key = False
        else:
            self.safe.interact(self.font)
            self.safe_message = self.safe.safe_message

        if self.safe.message:
            self.safe_message = self.safe.safe_message
            self.show_safe_message = True

            self.safe_message = self.font.render(self.safe.message, True,
                                                 (255, 255, 255))
            self.safe_message_rect = self.safe_message.get_rect(
                center=(self.rect.centerx, self.inventory_y - 30))
            self.message_timer = pg.time.get_ticks()

    def interact_with_radio(self):
        text_surface = self.font.render("Это радио. Сейчас оно просто шумит.", True, (255, 255, 255))  # Белый текст
        self.safe_message = text_surface
        self.safe_message_rect = text_surface.get_rect(
            center=(self.rect.centerx, self.inventory_y - 30))
        self.show_safe_message = True
        self.message_timer = pg.time.get_ticks()

    def interact_with_bed(self, inventory):
        """Выполняет действия при взаимодействии с кроватью."""
        item = self.bed.take_beads()
        if item:
            inventory.add_item(item)

        self.bed.interact()
        if self.bed.message:
            self.bed_message = self.bed.message
            self.bed_message_rect = self.bed.message.get_rect(
                center=(self.rect.centerx, self.inventory_y - 30))
            self.show_bed_message = True
            self.bed_message_timer = pg.time.get_ticks()
        else:
            self.bed_message = None
            self.bed_message_rect = None
            self.show_bed_message = False

    def interact_with_cupboard(self, inventory):
        item = self.cupboard.take_ring()
        if item:
            inventory.add_item(item)

        self.cupboard.interact(self.font)
        if self.cupboard.message:
            self.cupboard_message = self.font.render(self.cupboard.message, True, (255, 255, 255))
            self.cupboard_message_rect = self.cupboard_message.get_rect(
                center=(self.rect.centerx, self.inventory_y - 30))
            self.show_cupboard_message = True
            self.cupboard_message_timer = pg.time.get_ticks()
        else:
            self.cupboard_message = None
            self.cupboard_message_rect = None
            self.show_cupboard_message = False

    def interact_with_table(self, inventory):
        item = self.table.take_pasport()
        if item:
            inventory.add_item(item)
        self.table.interact(self.font)
        if self.table.message:
            self.table_message = self.font.render(self.table.message, True, (255, 255, 255))
            self.table_message_rect = self.table_message.get_rect(
                center=(self.rect.centerx, self.inventory_y - 30))
            self.show_table_message = True
            self.table_message_timer = pg.time.get_ticks()
        else:
            self.table_message = None
            self.table_message_rect = None
            self.show_table_message = False

    def check_all_items_collected(self, inventory):
        return "redring" in inventory.slots and "beads" in inventory.slots and "pasport" in inventory.slots

    def start_cutscene(self):
        self.show_cutscene = True
        self.cutscene = Cutscene(self.cutscene_phrases, self.font, self.screen_rect.width, self.screen_rect.height,(255, 0, 0))  # Красный цвет