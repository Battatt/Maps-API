import requests
import pygame
import os
import sys


class Window:
    def __init__(self, i_adress, i_params):
        self.adress = i_adress
        self.parameters = i_params
        self.map_file = "map.png"
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
                    if sp * 1.75 <= 100:
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

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((1000, 650))
        screen.fill((20, 20, 20))
        while True:
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
            self.update_image()
            pygame.draw.rect(screen, 'gray', (0, 80, 640, 490), 0)
            screen.blit(pygame.image.load(self.map_file), (15, 95))
            pygame.display.flip()


if __name__ == '__main__':
    spn = [0.5, 0.5]
    coords = [46.308014, 44.269656][::-1]
    search_params = {'ll': str(coords[0]) + ',' + str(coords[1]),
                     'spn': str(spn[0]) + ',' + str(spn[1]),
                     'l': 'map'}
    api_adress = "http://static-maps.yandex.ru/1.x/"
    app = Window(api_adress, search_params)
    app.run()
