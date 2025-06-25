import time
import threading
import pygame as pg

TIMER_EVENT = pg.USEREVENT + 1

class Timer:
    def __init__(self, duration, callback, event_type=TIMER_EVENT):
        self.duration = duration
        self.event_type = event_type
        self.remaining_time = duration
        self.running = False
        self.timer = None
        self.callback = callback

    def start(self):
        self.running = True
        self.timer = threading.Timer(1, self._tick)
        self.timer.start()

    def _tick(self):
        if self.running:
            self.remaining_time -= 1
            if self.remaining_time <= 0:
                self.stop()
                self.callback()
            else:
                self.timer = threading.Timer(1, self._tick)
                self.timer.start()

    def stop(self):
        self.running = False
        if self.timer:
            self.timer.cancel()
            self.timer = None

    def cancel(self):
        self.stop()

    def get_remaining_time(self):
        return self.remaining_time