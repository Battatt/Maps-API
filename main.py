from visual import Window


def main():
    spn = [0.5, 0.5]
    coords = [46.308014, 44.269656][::-1]
    search_params = {'ll': str(coords[0]) + ',' + str(coords[1]),
                     'spn': str(spn[0]) + ',' + str(spn[1]),
                     'l': 'map'}
    api_adress = "http://static-maps.yandex.ru/1.x/"
    app = Window(api_adress, search_params)
    app.run()


if __name__ == '__main__':
    main()
