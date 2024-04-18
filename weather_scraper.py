import requests
from bs4 import BeautifulSoup
from time import sleep
from collections import OrderedDict

def get_weather_data():

    # Задаем заголовки для запросов, чтобы выглядеть как обычный браузер
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107 Safari/537.36'
    }

    # Список месяцев для формирования URL
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

    # Словарь для хранения уникальных данных о погоде
    unique_data = OrderedDict()

    # Проходим по каждому месяцу
    for month in months:
        # Пауза между запросами для предотвращения блокировки сервером
        sleep(4)
        # Формируем URL для текущего месяца
        url = f'https://yandex.ru/pogoda/month/{month}?lat=54.985855&lon=73.28067&lang=ru&via=cnav'

        # Отправляем GET-запрос к URL с заданными заголовками
        response = requests.get(url, headers=headers)

        # Создаем объект BeautifulSoup для парсинга HTML-кода страницы
        soup = BeautifulSoup(response.text, 'lxml')

        # Извлекаем информацию о погоде для каждого дня месяца
        data = soup.find_all('div', class_='climate-calendar-day__detailed-container-center')

        # Проходим по каждому элементу с данными о погоде
        for i in data:
            # Извлекаем полное название дня и день недели
            data_day_full = i.find('h6', 'climate-calendar-day__detailed-day').text
            data_day, day_of_week = data_day_full.split(', ')

            # Извлекаем данные о температуре дня и ночи
            day_temperature = i.find('div', 'temp climate-calendar-day__detailed-basic-temp-day').text
            night_temperature = i.find('div', 'temp climate-calendar-day__detailed-basic-temp-night').text

            # Извлекаем числовое значение давления
            pressure_text = i.find('td',
                                   'climate-calendar-day__detailed-data-table-cell climate-calendar-day__detailed-data-table-cell_value_yes').text
            pressure_numeric = ''.join(filter(str.isdigit, pressure_text))

            # Извлекаем скорость ветра
            wind_speed = i.find('div', 'wind-speed').text

            # Извлекаем данные о направлении ветра
            road_wind = [abbr.get_text() for abbr in i.find_all('abbr', 'icon-abbr')]

            # Склеиваем строки из списка в одну строку
            road_wind = ', '.join(road_wind)

            # Проверяем, что данные о текущем дне еще не добавлены в словарь
            if (data_day, day_of_week, day_temperature, night_temperature, pressure_numeric, wind_speed, road_wind) not in unique_data.values():
                # Добавляем данные о погоде в словарь
                unique_data[data_day] = (data_day, day_of_week, day_temperature, night_temperature, pressure_numeric, wind_speed, road_wind)

    # Возвращаем список уникальных данных о погоде
    return list(unique_data.values())