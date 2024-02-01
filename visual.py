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

    def update_image(self, action=None):
        if action is None:
            response = requests.get(self.adress, params=self.parameters)

            if not response:
                """print("Ошибка выполнения запроса:")
                print("Http статус:", response.status_code, "(", response.reason, ")")"""
                return

            with open(self.map_file, "wb") as file:
                file.write(response.content)
        else:
            if action == 'spn_extend':
                temp_list = list(map(float, self.parameters['spn'].split(',')))
                res = ','.join(list(map(lambda x: str(x * 1.75), temp_list)))
                self.parameters['spn'] = res
            elif action == 'spn_reduce':
                temp_list = list(map(float, self.parameters['spn'].split(',')))
                res = ','.join(list(map(lambda x: str(x * 0.5), temp_list)))
                self.parameters['spn'] = res

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((600, 450))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    os.remove(self.map_file)
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_PAGEUP:
                        self.update_image(action='spn_extend')
                    if event.key == pygame.K_PAGEDOWN:
                        self.update_image(action='spn_reduce')
            self.update_image()
            screen.blit(pygame.image.load(self.map_file), (0, 0))
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
