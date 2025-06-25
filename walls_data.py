import pygame as pg
import pygame as pg
from wall import Wall

level_objects = {"left_wall":(1,1,9,256),
                 "right_wall":(312,0,322,256),
                 "top_wall":(1,1,322,11),
                 "bottom_wall": (1,246,175,256),
                 "exit":(176,256,257,255),
                 "wall_near_exit":(257,246,321,256),
                 "safe":(257,206,310,245),
                 "table":(11,218,63,245), #ЭТО ШКАФ
                 "cupboard":(109,228,148,245), #АПТЕЧКА
                 "bed":(11,12,59,96),
                 "radio":(240,12,276,23)}

def create_walls():
    walls = [Wall(*coords) for coords in level_objects.values()]
    return walls