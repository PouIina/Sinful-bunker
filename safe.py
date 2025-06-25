# safe.py
import pygame as pg

class Safe:
    def __init__(self, rect):
        self.rect = rect
        self.has_key = False  # Изначально ключа нет
        self.message = None
        self.key_message = "Ключ! Можно уходить!" # Сообщение при взаимодействии, когда ключ уже взят
        self.need_key_message = "Нужен код!"  # Сообщение, когда ключа нет
        self.safe_message = None # Сообщение сейфа

    def take_key(self):
        """Забирает ключ из сейфа, если он есть."""
        if self.has_key:
            self.has_key = False
            self.message = self.key_message  # Устанавливаем сообщение после взятия ключа
            return "key"
        else:
            self.message = None
            return None

    def interact(self, font):
        """Действия при взаимодействии с сейфом."""
        if self.has_key:
            self.message = self.key_message # Сообщение, если ключ найден
            self.safe_message = None
        else:
            self.message = self.need_key_message # Сообщение, если ключа нет
            self.safe_message = font.render(self.message, True, (255, 255, 255)) # Белый текст