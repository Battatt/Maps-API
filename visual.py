import requests
import pygame
import os
import sys


def visual_window(api_adress, search_params):
    print(api_adress)
    print(search_params)
    response = requests.get(api_adress, params=search_params)

    if not response:
        print("Ошибка выполнения запроса:")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
    os.remove(map_file)


if __name__ == '__main__':
    spn = [0.5, 0.5]
    coords = [46.308014, 44.269656][::-1]
    search_params = {'ll': str(coords[0]) + ',' + str(coords[1]),
                     'spn': str(spn[0]) + ',' + str(spn[1]),
                     'l': 'map'}
    api_adress = "http://static-maps.yandex.ru/1.x/"
    visual_window(api_adress, search_params)
