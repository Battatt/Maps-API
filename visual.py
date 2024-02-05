import requests
import pygame
import os
import sys
from objects import Button, TextInput


class Window:
    def __init__(self, i_adress, i_params):
        self.adress = i_adress
        self.width, self.height = 1000, 650
        self.parameters = i_params
        self.map_file = "map.png"
        self.log_adress = ''
        self.post = ''
        self.update_image()

    def update_image(self, action=None, movement=None):
        if action is None:
            response = requests.get(self.adress, params=self.parameters)

            if not response:
                print("Ошибка выполнения запроса:")
                print("Http статус:", response.status_code, "(", response.reason, ")")
                print("PARAMS:", self.parameters)
                return

            with open(self.map_file, "wb") as file:
                file.write(response.content)
        else:
            if action == 'spn_extend':
                temp_list = list(map(float, self.parameters['spn'].split(',')))
                res = []
                for sp in temp_list:
                    extend = sp
                    if sp * 1.75 <= 90:
                        extend *= 1.75
                    res.append(str(extend))
                res = ','.join(res)
                self.parameters['spn'] = res
            elif action == 'spn_reduce':
                temp_list = list(map(float, self.parameters['spn'].split(',')))
                res = []
                for sp in temp_list:
                    extend = sp
                    if sp * 0.5 >= 10 ** (-4):
                        extend *= 0.5
                    res.append(str(extend))
                res = ','.join(res)
                self.parameters['spn'] = res
            elif action == 'move':
                if movement is not None:
                    spn_x, spn_y = list(map(float, self.parameters['spn'].split(',')))
                    x_0, y_0 = list(map(float, self.parameters['ll'].split(',')))
                    x = x_0 - spn_x / 2 if movement == 'left' else x_0 + spn_x / 2 if movement == 'right' else x_0
                    y = y_0 - spn_y / 2 if movement == 'down' else y_0 + spn_y / 2 if movement == 'up' else y_0
                    x = 180 - spn_x / 2 if x < -180 else - 180 + spn_x / 2 if x > 180 else x
                    y = y_0 if y > 90 else y_0 if y < -90 else y
                    res = str(x) + ',' + str(y)
                    self.parameters['ll'] = res
            elif action in ['sat', 'skl', 'map']:
                self.parameters['l'] = action

    def search_object(self, name):
        if name is not None:
            response = requests.get(f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-"
                                    f"98533de7710b&geocode={name}&format=json")
            if not response:
                print("Ошибка выполнения запроса:")
                print("Http статус:", response.status_code, "(", response.reason, ")")
                print("PARAMS:", name)
                print('Не забывайте нажать Enter при вводе текста')
                return
            result = response.json()
            try:
                point = result['response']['GeoObjectCollection']['featureMember'][-1]['GeoObject']['Point']['pos']
                self.log_adress = result['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
                self.log_adress = self.log_adress["metaDataProperty"]["GeocoderMetaData"]["Address"]["formatted"]
                try:
                    self.post = result['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
                    self.post = self.post["metaDataProperty"]["GeocoderMetaData"]["Address"]
                    print(self.post)
                except Exception as e:
                    print(e)
                    pass
                point = point.split()
                if point:
                    point = ','.join(point)
                    self.parameters['ll'] = point
                    if 'pt' not in self.parameters.keys():
                        self.parameters['pt'] = f"{point},flag"
                    elif self.parameters['pt'] is None:
                        self.parameters['pt'] = f"{point},flag"
                    else:
                        self.parameters['pt'] = self.parameters['pt'] + f"~{point},flag"
                    self.update_image()
            except Exception as e:
                print(result)
                print(e)
                print('Ошибка при выполнении поискового запроса')
        else:
            print('Ошибка в вызове геокодера')
            print('Переданные параметры:', name)
            print('Не забывайте нажать Enter при вводе текста')
            return

    def reset(self):
        self.log_adress, self.post = '', ''
        self.parameters['pt'] = None
        self.update_image()

    def run(self):
        clock = pygame.time.Clock()
        pygame.init()
        font = pygame.font.Font(None, int(0.03 * self.width))
        screen = pygame.display.set_mode((self.width, self.height))
        text_input = TextInput(x=0.01 * self.width, y=0.01 * self.height, width=0.7 * self.width,
                               height=0.1 * self.height, image_name='white.png', screen_width=self.width)
        text = ''
        titles = ['SEARCH', 'MAP', 'SAT', 'SKL', 'RESET']
        buttons = []
        button_x, button_y = 0.79 * self.width, 0.01 * self.height
        button_width, button_height = 0.18 * self.width, 0.1 * self.height
        for i in range(len(titles)):
            buttons.append(Button(x=button_x, y=button_y + i * button_height + i * 10,
                                  image_name='green.png',
                                  width=button_width, height=button_height,
                                  text=titles[i], volume=0, screen_width=self.width))
        while True:
            screen.fill((20, 20, 20))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    os.remove(self.map_file)
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_PAGEUP:
                        self.update_image(action='spn_extend')
                    elif event.key == pygame.K_PAGEDOWN:
                        self.update_image(action='spn_reduce')
                    elif event.key == pygame.K_DOWN:
                        self.update_image(action='move', movement='down')
                    elif event.key == pygame.K_UP:
                        self.update_image(action='move', movement='up')
                    elif event.key == pygame.K_RIGHT:
                        self.update_image(action='move', movement='right')
                    elif event.key == pygame.K_LEFT:
                        self.update_image(action='move', movement='left')
                elif event.type == pygame.USEREVENT:
                    if event.button.text == 'MAP':
                        self.update_image(action='map')
                    elif event.button.text == 'SKL':
                        self.update_image(action='skl')
                    elif event.button.text == 'SAT':
                        self.update_image(action='sat')
                    elif event.button.text == 'SEARCH':
                        self.search_object(text)
                    elif event.button.text == 'RESET':
                        self.reset()
                for button in buttons:
                    button.handle_event(event)
                temp = text_input.handle_event(event)
                if temp is not None:
                    text = temp
            self.update_image()
            pygame.draw.rect(screen, 'gray', (0, 80, 750, 490), 0)
            screen.blit(pygame.image.load(self.map_file), (15, 95))
            for button in buttons:
                button.hovered_checker(pygame.mouse.get_pos())
                button.draw(screen)
            if self.log_adress:
                text_draw = font.render(self.log_adress, True, 'white')
                text_rect = pygame.rect.Rect(10, 550, 640, 200)
                screen.blit(text_draw, text_rect)
            text_input.draw(screen)
            pygame.display.flip()
            clock.tick(60)


if __name__ == '__main__':
    spn = [0.5, 0.5]
    coords = [46.308014, 44.269656][::-1]
    search_params = {'ll': str(coords[0]) + ',' + str(coords[1]),
                     'spn': str(spn[0]) + ',' + str(spn[1]),
                     'l': 'map'}
    api_adress = "http://static-maps.yandex.ru/1.x/"
    app = Window(api_adress, search_params)
    app.run()
