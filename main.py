import pygame as pg
import sys
import Menu
from introduction import run_introduction
from player import Player
from level1 import Level1
from level2 import Level2
from timer import Timer
from inventory import Inventory
from level3 import Level3
from final_screen import final_screen

def terminate():
    pg.quit()
    sys.exit()

def start_game(screen, level=1, player=None, inventory=None):
    sc_w, sc_h = 1600, 900

    def display_timer(screen, remaining_time, x, y, font_size=36):
        font = pg.font.Font(None, font_size)
        minutes, seconds = divmod(remaining_time, 60)
        time_string = "{:02d}:{:02d}".format(minutes, seconds)
        text_surface = font.render(time_string, True, (255, 255, 255))
        text_rect = text_surface.get_rect(topright=(x - 30, y + 20))
        return text_surface, text_rect

    if level == 1:
        level12 = Level1(sc_w, sc_h)
        hero = player if player else Player(sc_w, sc_h)
        hero.rect.center = level12.rect.center
        if inventory is None:
            inventory = Inventory(sc_w, sc_h)

    elif level == 2:
        level2 = Level2(sc_w, sc_h)
        hero = player if player else Player(sc_w, sc_h)
        hero.rect.x = 375
        hero.rect.y = 300
        if inventory is None:
            inventory = Inventory(sc_w, sc_h)

    elif level == 3:
        level3 = Level3(sc_w, sc_h)
        hero = player if player else Player(sc_w, sc_h)
        hero.rect.x = 670
        hero.rect.y = 570
        if inventory is None:
            inventory = Inventory(sc_w, sc_h)

    game_over = False
    game_timer = Timer(20, lambda: None)
    game_timer.start()
    run = True
    clock = pg.time.Clock()
    last_remaining_time = -1
    text_surface, text_rect = None, None

    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "exit"

            if event.type == pg.MOUSEBUTTONDOWN:
                inventory.select_slot_at_pos(event.pos)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return "menu"
                if level == 1:
                    if event.key == pg.K_f:
                        if level12.is_player_near_safe(hero.rect):
                            level12.interact_with_safe(inventory)
                        if level12.is_player_near_radio(hero.rect):
                            level12.interact_with_radio()
                        is_near_bed = level12.is_player_near_bed(hero.rect)
                        if is_near_bed:
                            level12.interact_with_bed(inventory)
                        if level12.is_player_near_cupboard(hero.rect):
                            level12.interact_with_cupboard(inventory)
                        if level12.is_player_near_table(hero.rect):
                            level12.interact_with_table(inventory)
                    if event.key == pg.K_SPACE and level12.show_cutscene:
                        if level12.cutscene.current_index < len(level12.cutscene.phrases) - 1:
                            level12.cutscene.next_phrase()
                        else:
                            level12.show_cutscene = False
                            inventory.slots = [None] * 10
                            level12.give_key_to_safe()

                if level == 2:
                    if event.key == pg.K_SPACE and level2.show_cutscene:
                        if level2.cutscene.current_index < len(level2.cutscene.phrases) - 1:
                            level2.cutscene.next_phrase()
                        else:
                            level2.show_cutscene = False
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_f:
                            if level2.is_player_near_tables(hero.rect):
                                level2.interact_with_tables()
                            if level2.is_player_near_pork(hero.rect):
                                level2.interact_with_pork(inventory)
                            if level2.is_player_near_closet(hero.rect):
                                level2.interact_with_closet(inventory)
                            if level2.is_player_near_box1(hero.rect):
                                level2.interact_with_box1(inventory)
                            if level2.is_player_near_box2(hero.rect):
                                level2.interact_with_box2()
                            if level2.is_player_near_greenboxes(hero.rect):
                                level2.interact_with_greenboxes()
                            if level2.is_player_near_rpanel(hero.rect):
                                level2.interact_with_rpanel()
                            if level2.is_player_near_lpanel(hero.rect):
                                level2.interact_with_lpanel()
                            if level2.is_player_near_wire(hero.rect):
                                level2.interact_with_wire(inventory)
                if level == 3:
                    if event.key == pg.K_SPACE and level3.show_cutscene:
                        if level3.cutscene.current_index < len(level3.cutscene.phrases) - 1:
                            level3.cutscene.next_phrase()
                        else:
                            level3.show_cutscene = False
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_f:
                            if level3.is_player_near_radio(hero.rect):
                                level3.interact_with_radio()
                    if level3.show_radio_cutscene and event.key == pg.K_SPACE:
                        if level3.radio_cutscene.current_index < len(level3.radio_cutscene.phrases) - 1:
                            level3.radio_cutscene.next_phrase()
                        else:
                            level3.show_radio_cutscene = False

        if game_timer.running:
            remaining_time = game_timer.get_remaining_time()
            if remaining_time != last_remaining_time:
                text_surface, text_rect = display_timer(screen, remaining_time, sc_w - 10, 10)
                last_remaining_time = remaining_time
        else:
            return final_screen(screen, sc_w, sc_h, "Конец игры!")

        keys = pg.key.get_pressed()

        screen.fill('black')

        if level == 1:
            level12.draw(screen, hero)
            hero.move(keys, [], level12.walls)

            if level12.exit_trigger.is_colliding(hero.rect):
                game_timer.cancel()
                level12.stop_music()
                return start_game(screen, level=2, player=hero, inventory=inventory)

            level12.update(hero, inventory)
            if level12.check_all_items_collected(inventory) and not level12.show_cutscene:
                level12.start_cutscene()

        elif level == 2:
            level2.draw(screen, hero)
            hero.move(keys, [], level2.walls)
            level2.update(hero, inventory)

            if level2.exit_trigger.is_colliding(hero.rect):
                level2.stop_music()
                game_timer.cancel()
                return start_game(screen, level=3, player=hero, inventory=inventory)
        elif level == 3:
            level3.draw(screen, hero)
            hero.move(keys, [], level3.walls)
            level3.update(hero)
            if level3.final_exit_trigger.is_colliding(hero.rect):
                game_timer.cancel()
                return final_screen(screen, sc_w, sc_h, "Поздравляю, вы победили!")

        hero.draw(screen)
        inventory.draw(screen)

        if text_surface is not None and text_rect is not None:
            screen.blit(text_surface, text_rect)

        pg.display.update()
        clock.tick(60)

    if level == 1:
        level12.stop_music()
    elif level == 2:
        level2.stop_music()
    return "menu"

def main():
    pg.init()
    pg.display.set_caption('MAIN MENU')
    WIDTH, HEIGHT = 1600, 900
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.font.init()
    clock = pg.time.Clock()

    while True:
        choice = Menu.main_menu(screen)

        if choice == "play":
            if run_introduction(screen):
                result = start_game(screen)
                if result == "exit":
                    break
            else:
                break

        elif choice == "exit":
            break
    terminate()

if __name__ == "__main__":
    main()