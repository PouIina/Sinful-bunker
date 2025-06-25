import pygame as pg
from wall import Wall
from cutscene import Cutscene
from level2_walls import level_objects
from closet import Closet
from box1 import Box1
from exit_zone import ExitTrigger

class Level2:
    def __init__(self, screen_width, screen_height):
        pg.mixer.init()
        pg.font.init()
        self.font = pg.font.Font(None, 30)
        pg.mixer.music.load('assets/DyingLight.mp3')
        pg.mixer.music.play(-1)

        self.original_image = pg.image.load("assets/вторая/ВТОРАЯ КОМНАТА.png").convert_alpha()
        self.scale_factor = 1.5
        self.scaled_image = self.original_image
        self.rect = self.scaled_image.get_rect()
        self.screen_rect = pg.Rect(0, 0, screen_width, screen_height)

        self.inventory_y = 700

        self.table_message = None
        self.table_message_rect = None
        self.show_table_message = False
        self.table_message_timer = 0
        self.has_read_table_note = False

        self.rpanel_message = None
        self.rpanel_message_rect = None
        self.show_rpanel_message = False
        self.rpanel_message_timer = 0
        self.is_right_panel_active = False

        self.lpanel_message = None
        self.lpanel_message_rect = None
        self.show_lpanel_message = False
        self.lpanel_message_timer = 0
        self.is_left_panel_active = False

        self.box2_message = None
        self.box2_message_rect = None
        self.show_box2_message = False
        self.box2_message_timer = 0
        self.has_read_box2_note = False

        self.pork_message = None
        self.pork_message_rect = None
        self.show_pork_message = False
        self.pork_message_timer = 0
        self.is_pizza_on_plate = False

        self.wire_message = None
        self.wire_message_rect = None
        self.show_wire_message = False
        self.wire_message_timer = 0
        self.is_wire_cutted = False

        self.level_objects = level_objects
        self.walls = [Wall(*coords) for coords in self.level_objects.values()]
        self._setup_level()
        self.closet = Closet(pg.Rect(self.level_objects["closet"][0], self.level_objects["closet"][1], self.level_objects["closet"][2], self.level_objects["closet"][3]))
        self.box1 = Box1(pg.Rect(self.level_objects["box1"][0], self.level_objects["box1"][1], self.level_objects["box1"][2], self.level_objects["box1"][3]))

        self.closet_message = None
        self.closet_message_rect = None
        self.show_closet_message = False
        self.closet_message_timer = 0

        self.box1_message = None
        self.box1_message_rect = None
        self.show_box1_message = False
        self.box1_message_timer = 0

        self.green_boxes_message = None
        self.green_boxes_message_rect = None
        self.show_green_boxes_message = False
        self.green_boxes_message_timer = 0
        self.has_read_greenboxes_note = False

        self.exit_trigger = ExitTrigger(736 * self.scale_factor, -1 * self.scale_factor, 817 * self.scale_factor, 10 * self.scale_factor)  # Примерные координаты и размеры
        self.exit_trigger.rect.x += self.rect.x
        self.exit_trigger.rect.y += self.rect.y
        self.level3_transition_active = False


        self.cutscene_phrases = [
            "Неплохо.",
            "Так и не понял, почему ты здесь?",
            "У тебя не так много времени на обдумывание.",
            "Суд идёт. Подсудимый - ты.",
            "Может, всё-таки решишь вспомнить свои деяния?",
        ]
        self.cutscene = Cutscene(self.cutscene_phrases, self.font, screen_width, screen_height, (255, 255, 255))
        self.show_cutscene = True

    def _setup_level(self):
        new_size = (
            int(self.original_image.get_width() * self.scale_factor),
            int(self.original_image.get_height() * self.scale_factor)
        )
        self.scaled_image = pg.transform.scale(self.original_image, new_size)
        self.rect = self.scaled_image.get_rect()

        for wall in self.walls:
            wall.update_scale(self.scale_factor)

        self.rect.center = self.screen_rect.center
        offset_x = self.rect.x
        offset_y = self.rect.y

        for wall in self.walls:
            wall.apply_offset(offset_x, offset_y)


    def is_player_near_tables(self, player_rect):
        x = 478 * self.scale_factor
        y = 10 * self.scale_factor
        width = (665 - 478) * self.scale_factor
        height = (28 - 10) * self.scale_factor

        tables_rect = pg.Rect(x + self.rect.x, y + self.rect.y, width,height)
        tables_center_x = tables_rect.centerx
        tables_center_y = tables_rect.centery
        distance = ((player_rect.centerx - tables_center_x) ** 2 + (player_rect.centery - tables_center_y) ** 2) ** 0.5
        interaction_radius = 100
        return distance < interaction_radius

    def interact_with_tables(self):
        text_surface = self.font.render("Какая-то инструкция. Для закрытия двери 2 подключите красный провод.", True, (255, 255, 255))
        self.table_message = text_surface
        self.has_read_table_note = True
        self.table_message_rect = text_surface.get_rect(center=(self.rect.centerx, self.inventory_y - 30))
        self.show_table_message = True
        self.table_message_timer = pg.time.get_ticks()

    def is_player_near_closet(self, player_rect):
        x = self.level_objects["closet"][0] * self.scale_factor
        y = self.level_objects["closet"][1] * self.scale_factor
        width = (self.level_objects["closet"][2] - self.level_objects["closet"][0]) * self.scale_factor
        height = (self.level_objects["closet"][3] - self.level_objects["closet"][1]) * self.scale_factor

        closet_rect = pg.Rect(x + self.rect.x, y + self.rect.y, width,height)

        closet_center_x = closet_rect.centerx
        closet_center_y = closet_rect.centery

        distance = ((player_rect.centerx - closet_center_x) ** 2 + (player_rect.centery - closet_center_y) ** 2) ** 0.5

        interaction_radius = 100
        return distance < interaction_radius

    def interact_with_closet(self, inventory):
        self.closet.interact(self.font, inventory)
        self.closet_message = self.closet.message
        self.closet_message_rect = self.closet.message.get_rect(
            center=(self.rect.centerx, self.inventory_y - 30))
        self.show_closet_message = True
        self.closet_message_timer = pg.time.get_ticks()

    def is_player_near_box1(self, player_rect):
        x = self.level_objects["box1"][0] * self.scale_factor
        y = self.level_objects["box1"][1] * self.scale_factor
        width = (self.level_objects["box1"][2] - self.level_objects["box1"][0]) * self.scale_factor
        height = (self.level_objects["box1"][3] - self.level_objects["box1"][1]) * self.scale_factor

        box1_rect = pg.Rect(x + self.rect.x, y + self.rect.y, width,height)

        box1_center_x = box1_rect.centerx
        box1_center_y = box1_rect.centery
        distance = ((player_rect.centerx - box1_center_x) ** 2 + (player_rect.centery - box1_center_y) ** 2) ** 0.5
        interaction_radius = 50
        return distance < interaction_radius

    def interact_with_box1(self, inventory):
        self.box1.interact(self.font, inventory)
        self.box1_message = self.box1.message
        self.box1_message_rect = self.box1.message.get_rect(
            center=(self.rect.centerx, self.inventory_y - 30))
        self.show_box1_message = True
        self.box1_message_timer = pg.time.get_ticks()

    def is_player_near_pork(self, player_rect):
        x = 11 * self.scale_factor
        y = 91 * self.scale_factor
        width = (28 - 11) * self.scale_factor
        height = (128 - 91) * self.scale_factor
        pork_rect = pg.Rect(x + self.rect.x, y + self.rect.y, width, height)
        tables_center_x = pork_rect.centerx
        tables_center_y = pork_rect.centery
        distance = ((player_rect.centerx - tables_center_x) ** 2 + (player_rect.centery - tables_center_y) ** 2) ** 0.5
        interaction_radius = 50
        return distance < interaction_radius

    def interact_with_pork(self, inventory):
        if not self.has_read_greenboxes_note:
            text_surface = self.font.render("Пыльная тарелка.", True, (255, 255, 255))
        elif self.is_pizza_on_plate:
            text_surface = self.font.render("Пыльная пицца на пыльной тарелке.", True, (255, 255, 255))
        elif "pizza" in [self.slots for self.slots in inventory.slots]:
            text_surface = self.font.render("Пожалуй, это должно лежать здесь.", True, (255, 255, 255))
            for i in range(len(inventory.slots)):
                if inventory.slots[i] == "pizza":
                    inventory.slots[i] = None
                    break
            self.is_pizza_on_plate = True
        else:
            text_surface = self.font.render("Похоже, кто-то требует пиццу.", True, (255, 255, 255))
        self.pork_message = text_surface
        self.pork_message_rect = text_surface.get_rect(center=(self.rect.centerx, self.inventory_y - 30))
        self.show_pork_message = True
        self.pork_message_timer = pg.time.get_ticks()

    def is_player_near_box2(self, player_rect):
        x = 100 * self.scale_factor
        y = 197 * self.scale_factor
        width = (136 - 100) * self.scale_factor
        height = (224 - 197) * self.scale_factor
        box2_rect = pg.Rect(x + self.rect.x, y + self.rect.y, width, height)
        box2_center_x = box2_rect.centerx
        box2_center_y = box2_rect.centery
        distance = ((player_rect.centerx - box2_center_x) ** 2 + (player_rect.centery - box2_center_y) ** 2) ** 0.5
        interaction_radius = 50
        return distance < interaction_radius

    def interact_with_box2(self):
        if not self.has_read_box2_note:
            text_surface = self.font.render("Запика: left-3, right-5.", True, (255, 255, 255))
            self.box2_message = text_surface
            self.has_read_box2_note = True

            self.box2_message_rect = text_surface.get_rect(center=(self.rect.centerx, self.inventory_y - 30))
            self.show_box2_message = True
            self.box2_message_timer = pg.time.get_ticks()

    def is_player_near_greenboxes(self, player_rect):
        x = 555 * self.scale_factor
        y = 166 * self.scale_factor
        width = (620 - 555) * self.scale_factor
        height = (225 - 166) * self.scale_factor
        green_boxes_rect = pg.Rect(x + self.rect.x, y + self.rect.y, width, height)
        green_boxes_center_x = green_boxes_rect.centerx
        green_boxes_center_y = green_boxes_rect.centery

        distance = ((player_rect.centerx - green_boxes_center_x) ** 2 + (player_rect.centery - green_boxes_center_y) ** 2) ** 0.5
        interaction_radius = 100
        return distance < interaction_radius

    def interact_with_greenboxes(self):
        text_surface = self.font.render("Запика: Я люблю пиццу. Покорми меня.", True, (255, 255, 255))
        self.green_boxes_message = text_surface
        self.has_read_greenboxes_note = True  # Прочитали записку
        self.green_boxes_message_rect = text_surface.get_rect(center=(self.rect.centerx, self.inventory_y - 30))
        self.show_green_boxes_message = True
        self.green_boxes_message_timer = pg.time.get_ticks()  # Важно!

    def is_player_near_rpanel(self, player_rect):
        x = 11 * self.scale_factor
        y = 36 * self.scale_factor
        width = (19 - 11) * self.scale_factor
        height = (73 - 36) * self.scale_factor
        rpanel_rect = pg.Rect(x + self.rect.x, y + self.rect.y, width, height)
        rpanel_center_x = rpanel_rect.centerx
        rpanel_center_y = rpanel_rect.centery
        distance = ((player_rect.centerx - rpanel_center_x) ** 2 + (player_rect.centery - rpanel_center_y) ** 2) ** 0.5
        interaction_radius = 50
        return distance < interaction_radius

    def interact_with_rpanel(self):
        if not self.has_read_box2_note:
            text_surface = self.font.render("Какие-то странные цифры.", True, (255, 255, 255))
        else:
            text_surface = self.font.render("Ввожу цифру 5...", True, (255, 255, 255))
            self.is_right_panel_active = True

        self.rpanel_message = text_surface
        self.rpanel_message_rect = text_surface.get_rect(center=(self.rect.centerx, self.inventory_y - 30))
        self.show_rpanel_message = True
        self.rpanel_message_timer = pg.time.get_ticks()

    def is_player_near_lpanel(self, player_rect):
        x = 11 * self.scale_factor
        y = 146 * self.scale_factor
        width = (19 - 11) * self.scale_factor
        height = (183 - 146) * self.scale_factor
        lpanel_rect = pg.Rect(x + self.rect.x, y + self.rect.y, width, height)
        lpanel_center_x = lpanel_rect.centerx
        lpanel_center_y = lpanel_rect.centery

        distance = ((player_rect.centerx - lpanel_center_x) ** 2 + (player_rect.centery - lpanel_center_y) ** 2) ** 0.5
        interaction_radius = 50
        return distance < interaction_radius

    def interact_with_lpanel(self):
        """Действия при взаимодействии с  (правым щитком)."""
        if not self.has_read_box2_note:
            text_surface = self.font.render("Похоже на азбуку Морзе.", True, (255, 255, 255))
        else:
            text_surface = self.font.render("Нажимаю 3-ю кнопку.", True, (255, 255, 255))
            self.is_left_panel_active = True  # Активируем правый щиток

        self.lpanel_message = text_surface  # Сохраняем сообщение
        self.lpanel_message_rect = text_surface.get_rect(center=(self.rect.centerx, self.inventory_y - 30))
        self.show_lpanel_message = True
        self.lpanel_message_timer = pg.time.get_ticks()

    def is_player_near_wire(self, player_rect):
        x = 45 * self.scale_factor
        y = 11 * self.scale_factor
        width = (129 - 45) * self.scale_factor
        height = (19 - 11) * self.scale_factor
        wire_rect = pg.Rect(x + self.rect.x, y + self.rect.y, width, height)
        wire_center_x = wire_rect.centerx
        wire_center_y = wire_rect.centery
        distance = ((player_rect.centerx - wire_center_x) ** 2 + (player_rect.centery - wire_center_y) ** 2) ** 0.5
        interaction_radius = 50
        return distance < interaction_radius

    def interact_with_wire(self, inventory):
        if not self.has_read_table_note:
            text_surface = self.font.render("Панель с проводами.", True, (255, 255, 255))
        elif "cutters" in [self.slots for self.slots in inventory.slots] and not self.is_wire_cutted:
            text_surface = self.font.render("Настало время прорубить себе выход!.", True, (255, 255, 255))
            self.is_wire_cutted = True
        elif self.is_wire_cutted:
            text_surface = self.font.render("Теперь здесь всё искрится.", True, (255, 255, 255))
        else:
            text_surface = self.font.render("Нужен острый предмет.", True, (255, 255, 255))
        self.wire_message = text_surface
        self.wire_message_rect = text_surface.get_rect(center=(self.rect.centerx, self.inventory_y - 30))
        self.show_wire_message = True
        self.wire_message_timer = pg.time.get_ticks()

    def check_level2_complete(self, inventory):
        """Проверяет, выполнены ли все условия для перехода на 3 уровень."""
        return (self.is_wire_cutted and self.is_pizza_on_plate and self.is_left_panel_active and self.is_right_panel_active
                )


    def update(self, player, inventory):
        if self.show_cutscene:
            self.cutscene.update()
            if self.cutscene.done:
                self.show_cutscene = False
            return

        for wall in self.walls:
            if player.rect.colliderect(wall.rect):
                return True

        level2_complete = self.check_level2_complete(inventory)

        if level2_complete:
            self.exit_trigger.activate()
        else:
            self.exit_trigger.deactivate()

        if self.exit_trigger.is_colliding(player.rect):
            self.level3_transition_active = True

        if self.show_table_message:  # А нужно ли его показывать?
            time_elapsed = pg.time.get_ticks() - self.table_message_timer
            if time_elapsed > 2000:
                self.show_table_message = False
                self.table_message = None
                self.table_message_rect = None

        if self.show_pork_message:
            time_elapsed = pg.time.get_ticks() - self.pork_message_timer
            if time_elapsed > 2000:
                self.show_pork_message = False
                self.pork_message = None
                self.pork_message_rect = None


        if self.show_closet_message:
            if pg.time.get_ticks() - self.closet_message_timer > 2000:
                self.show_closet_message = False
                self.closet_message = None
                self.closet_message_rect = None

        if self.show_box1_message:
            if pg.time.get_ticks() - self.box1_message_timer > 2000:
                self.show_box1_message = False
                self.box1_message = None
                self.box1_message_rect = None

        if self.show_box2_message:
            if pg.time.get_ticks() - self.box2_message_timer > 2000:
                self.show_box2_message = False
                self.box2_message = None
                self.box2_message_rect = None

        if self.show_green_boxes_message:
            if pg.time.get_ticks() - self.green_boxes_message_timer > 2000:
                self.show_green_boxes_message = False
                self.green_boxes_message = None
                self.green_boxes_message_rect = None

        if self.show_rpanel_message:
            if pg.time.get_ticks() - self.rpanel_message_timer > 2000:
                self.show_rpanel_message = False
                self.rpanel_message = None
                self.rpanel_message_rect = None

        if self.show_lpanel_message:
            if pg.time.get_ticks() - self.lpanel_message_timer > 2000:
                self.show_lpanel_message = False
                self.lpanel_message = None
                self.lpanel_message_rect = None

        if self.show_wire_message:
            if pg.time.get_ticks() - self.wire_message_timer > 2000:
                self.show_wire_message = False
                self.wire_message = None
                self.wire_message_rect = None

        return False

    def draw(self, surface, player):
        surface.blit(self.scaled_image, self.rect)
        for wall in self.walls:
            wall.draw(surface)


        if self.show_table_message and self.table_message and self.table_message_rect:
            surface.blit(self.table_message, self.table_message_rect)
        #тарелька
        if self.show_pork_message and self.pork_message and self.pork_message_rect:
            surface.blit(self.pork_message, self.pork_message_rect)
        #Шкафь
        if self.show_closet_message and self.closet_message and self.closet_message_rect:
            surface.blit(self.closet_message, self.closet_message_rect)

        if self.show_box1_message and self.box1_message and self.box1_message_rect:
            surface.blit(self.box1_message, self.box1_message_rect)
        if self.show_box2_message and self.box2_message and self.box2_message_rect:
            surface.blit(self.box2_message, self.box2_message_rect)
        if self.show_green_boxes_message and self.green_boxes_message and self.green_boxes_message_rect:
            surface.blit(self.green_boxes_message, self.green_boxes_message_rect)
        if self.show_rpanel_message and self.rpanel_message and self.rpanel_message_rect:
            surface.blit(self.rpanel_message, self.rpanel_message_rect)
        if self.show_lpanel_message and self.lpanel_message and self.lpanel_message_rect:
            surface.blit(self.lpanel_message, self.lpanel_message_rect)
        if self.show_wire_message and self.wire_message and self.wire_message_rect:
            surface.blit(self.wire_message, self.wire_message_rect)

        if self.show_cutscene:
            self.cutscene.draw(surface)

    def stop_music(self):
        pg.mixer.music.stop()