import requests
import pygame
import os
import sys


def visual_window(request):
    response = requests.get(request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запишем полученное изображение в файл.
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    # Инициализируем pygame
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    # Рисуем картинку, загружаемую из только что созданного файла.
    screen.blit(pygame.image.load(map_file), (0, 0))
    # Переключаем экран и ждем закрытия окна.
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()

    # Удаляем за собой файл с изображением.
    os.remove(map_file)


if __name__ == '__main__':
    visual_window("http://static-maps.yandex.ru/1.x/?ll=44.301532,46.307033&spn=0.01,0.01&l=map")
