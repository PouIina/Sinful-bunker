import pygame as pg

class Player:
    def __init__(self, screen_width, screen_height, size=40):
        self.original_sprites = {  # загрузка спрайтов
            'left_small': pg.image.load('assets/гг/левая меньше.png').convert_alpha(),
            'left_big': pg.image.load('assets/гг/левая больше.png').convert_alpha(),
            'right_small': pg.image.load('assets/гг/правая меньше.png').convert_alpha(),
            'right_big': pg.image.load('assets/гг/правая больше.png').convert_alpha(),
            'idle': pg.image.load('assets/гг/стоит.png').convert_alpha()
        }

        self.size = size
        self.sprites = {}
        for name, surf in self.original_sprites.items():
            self.sprites[name] = pg.transform.scale(surf, (size, size))

        self.current_sprite = 'idle'
        self.animation_phase = 0
        self.animation_speed = 0.2
        self.last_update = 0

        self.rect = self.sprites['idle'].get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.speed = 5
        self.direction = 'down'
        self.diagonal = 0.7

    def rotate_sprite(self, sprite, direction):
        if direction == 'up':
            return pg.transform.rotate(sprite, 180)
        elif direction == 'up_left':
            return pg.transform.rotate(sprite, -135)
        elif direction == 'up_right':
            return pg.transform.rotate(sprite, 135)
        elif direction == 'left':
            return pg.transform.rotate(sprite, -90)
        elif direction == 'right':
            return pg.transform.rotate(sprite, 90)
        elif direction == 'down_left':
            return pg.transform.rotate(sprite, -45)
        elif direction == 'down_right':
            return pg.transform.rotate(sprite, 45)
        else:
            return sprite

    def move(self, keys, boxes=[], walls=None):
        old_rect = self.rect.copy()
        moving = False
        x_move, y_move = 0, 0

        if keys[pg.K_a]: x_move -= 1
        if keys[pg.K_d]: x_move += 1
        if keys[pg.K_w]: y_move -= 1
        if keys[pg.K_s]: y_move += 1

        if x_move != 0 or y_move != 0:
            moving = True
            if x_move != 0 and y_move != 0:
                x_move *= self.diagonal
                y_move *= self.diagonal

            self.rect.x += x_move * self.speed
            self.rect.y += y_move * self.speed

            if y_move < 0:
                if x_move < 0:
                    self.direction = 'up_left'
                elif x_move > 0:
                    self.direction = 'up_right'
                else:
                    self.direction = 'up'
            elif y_move > 0:
                if x_move < 0:
                    self.direction = 'down_left'
                elif x_move > 0:
                    self.direction = 'down_right'
                else:
                    self.direction = 'down'
            else:
                if x_move < 0:
                    self.direction = 'left'
                else:
                    self.direction = 'right'

        now = pg.time.get_ticks()
        if moving:
            if now - self.last_update > self.animation_speed * 1000:
                self.last_update = now
                self.animation_phase = (self.animation_phase + 1) % 6

                if self.animation_phase == 0:
                    self.current_sprite = 'left_small'
                elif self.animation_phase == 1:
                    self.current_sprite = 'left_big'
                elif self.animation_phase == 2:
                    self.current_sprite = 'left_small'
                elif self.animation_phase == 3:
                    self.current_sprite = 'idle'
                elif self.animation_phase == 4:
                    self.current_sprite = 'right_small'
                elif self.animation_phase == 5:
                    self.current_sprite = 'right_big'
        else:
            self.current_sprite = 'idle'
            self.animation_phase = 0

        if walls:
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    self.rect = old_rect
                    break

    def draw(self, surface):
        sprite = self.sprites[self.current_sprite]

        rotated_sprite = self.rotate_sprite(sprite, self.direction)

        new_rect = rotated_sprite.get_rect(center=self.rect.center)

        surface.blit(rotated_sprite, new_rect)
        self.rect = new_rect