import pygame as pg

def run_introduction(screen):
    """Функция для запуска вступления."""
    sc_w, sc_h = 1600, 900

    # Диалоги (текст)
    dialogues = [
        "Чтож...",
        "Ты оказался в ловушке. И в этом виноват ты.",
        "У тебя есть ограниченное время, чтобы найти выход.",
        "С головоломками разберёшься сам.",
        "Развлекайся!"  # Последняя реплика
    ]
    current_dialogue_index = 0
    font = pg.font.Font(None, 36)
    text_color = (255, 255, 255)
    dialogue_box_color = (50, 50, 50)
    dialogue_box_height = 150  # Высота области для текста

    # Функция для отображения текста
    def draw_dialogue(text):
        dialogue_box = pg.Surface((sc_w, dialogue_box_height))
        dialogue_box.fill(dialogue_box_color)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(sc_w // 2, dialogue_box_height // 2))
        dialogue_box.blit(text_surface, text_rect)
        screen.blit(dialogue_box, (0, sc_h - dialogue_box_height))

    # Основной цикл вступления
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False  # Выход из игры
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:  # Переход к следующей реплике по нажатию пробела
                    # Сначала проверяем, не достигли ли мы конца списка
                    if current_dialogue_index + 1 >= len(dialogues):
                        running = False  # Завершение вступления
                    else:
                        current_dialogue_index += 1 #Только если не достигли конца, увеличиваем индекс

        screen.fill((0, 0, 0))  # Очистка экрана

        # Отображаем текущий диалог
        draw_dialogue(dialogues[current_dialogue_index])

        pg.display.flip()

    return True  # Если вступление завершилось успешно