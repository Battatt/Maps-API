import os
import pygame


def load_image(name, color_key=None):
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as e:
        print('Cannot open image', e)
        return None

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        if color_key == -2:
            color_key = "white"
            image.set_colorkey(color_key)
            image = pygame.transform.flip(image.copy(), True, False)
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def load_sound(name):
    fullname = os.path.join('sounds', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as e:
        print('Cannot open sound', e)
        return None
    else:
        return sound
