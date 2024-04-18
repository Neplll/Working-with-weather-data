import pandas as pd
import dateparser
import re
from openpyxl.utils.dataframe import dataframe_to_rows
from weather_scraper import get_weather_data
from openpyxl import Workbook

def clean_data_and_convert_types(weather_data):
    # Заменяем символ "−" на "-"
    weather_data = weather_data.apply(lambda x: x.map(lambda val: re.sub('−', '-', str(val))))

    # Преобразуем тип данных столбцов C, D, E в int
    weather_data[['Температура днем, °С', 'Температура ночью, °С', 'Давление, мм.рт.ст']] = \
        weather_data[['Температура днем, °С', 'Температура ночью, °С', 'Давление, мм.рт.ст']].astype(int)

    # Преобразуем тип данных столбца F в float
    weather_data['Скорость ветра, м/с'] = weather_data['Скорость ветра, м/с'].astype(float)

    # Преобразуем формат даты из "1 января" в "дд.мм.гг"
    weather_data['Дата'] = weather_data['Дата'].apply(lambda x: dateparser.parse(x, languages=['ru']).strftime('%d.%m.%y'))

    return weather_data

def write_weather_data_to_excel(weather_data_get, filename):
    # Создание DataFrame
    df = pd.DataFrame(weather_data_get,
                      columns=['Дата', 'День недели', 'Температура днем, °С', 'Температура ночью, °С',
                               'Давление, мм.рт.ст', 'Скорость ветра, м/с', 'Направление ветра'])

    # Очистка данных и преобразование типов
    df = clean_data_and_convert_types(df)

    # Создание документа Excel
    wb = Workbook()
    ws = wb.active

    # Запись данных из DataFrame в лист Excel
    for r_idx, row in enumerate(dataframe_to_rows(df, index=False), 1):
        ws.append(row)

    # Установка размера ячеек
    for column_cells in ws.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        ws.column_dimensions[column_cells[0].column_letter].width = length + 2

    # Сохранение файла Excel
    wb.save(filename)

    return df

write_weather_data_to_excel(get_weather_data(), 'temp_data.xlsx')