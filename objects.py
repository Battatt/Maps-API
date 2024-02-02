import pygame
from functions import load_image, load_sound


class Button:
    def __init__(self, x, y, width, height, text, image_name, volume, screen_width, hover_image_name=None,
                 sound_name=None, color_key=None):
        self.x, self.y, self.width, self.height, self.volume = x, y, width, height, volume
        self.screen_width = screen_width
        self.text = text
        self.image = load_image(image_name, color_key=color_key)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.hover_image = self.image
        self.hover_image_name = hover_image_name
        if self.hover_image_name:
            self.hover_image = pygame.transform.scale(load_image(self.hover_image_name, color_key=color_key),
                                                      (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.sound = load_sound(sound_name) if sound_name else None
        self.is_hovered = False

    def draw(self, surface):
        top_image = self.hover_image if self.is_hovered else self.image
        surface.blit(top_image, self.rect.topleft)
        font = pygame.font.Font(None, int(0.03 * self.screen_width))

        text_surface = font.render(self.text, True, 'white')
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def hovered_checker(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def update(self, surface, new_button_x, new_button_y, new_w, new_h):
        self.x, self.y, self.width, self.height = new_button_x, new_button_y, new_w, new_h
        self.screen_width = surface.get_width()
        self.image = pygame.transform.scale(self.image, (new_w, new_h))
        self.rect = self.image.get_rect(topleft=(new_button_x, new_button_y))
        self.hover_image = self.image
        if self.hover_image_name:
            self.hover_image = pygame.transform.scale(load_image(self.hover_image_name), (new_w, new_h))
        self.draw(surface)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.sound:
                self.sound.set_volume(self.volume / 100)
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))


class TextInput:
    def __init__(self, x, y, width, height, image_name, screen_width, only_digits: bool = False):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.screen_width = screen_width
        self.text = ''
        self.image = load_image(image_name)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.counter = 0
        self.text_input_flag = False
        self.is_hovered = False
        self.only_digits = only_digits
        self.__color = ""

    def draw(self, surface):
        self.counter += 1
        surface.blit(self.image, self.rect.topleft)
        font = pygame.font.Font(None, int(0.03 * self.screen_width))
        self.text = (self.text.replace('|', '') if self.text_input_flag and self.counter == 5 and '|' in self.text
                     else self.text + "|" if self.text_input_flag and self.counter < 5 and '|' not in self.text
                     else self.text)
        self.counter = self.counter if self.counter < 100 else 0

        color = 'black' if self.text_input_flag else 'green'

        text_surface = font.render(self.text[:35] if len(self.text) <= 35 else self.text[len(self.text) - 35:],
                                   True, color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def update(self, new_text_x, new_text_y, new_w, new_h):
        self.x, self.y, self.width, self.height = new_text_x, new_text_y, new_w, new_h
        self.image = pygame.transform.scale(self.image, (new_w, new_h))
        self.rect = self.image.get_rect(topleft=(new_text_x, new_text_y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.text_input_flag = True
            else:
                self.text_input_flag = False
        elif event.type == pygame.KEYDOWN and self.text_input_flag:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text.replace('|', '')
                self.text = self.text[:-1]
                self.text += "|"
            elif event.key == pygame.K_RETURN:
                self.text = self.text.replace('|', '')
                self.text_input_flag = False
                return self.text
            elif self.only_digits is False or event.unicode.isdigit():
                self.text = self.text.replace('|', '')
                self.text += event.unicode
                self.text += "|"
        return None
