import weather_api
import mysql.connector


def search_weather():
    city_name = input("Введите город для поиска: \n")
    connection = mysql.connector.connect(
        host="MySQL-8.2",
        user="root",
        password="",
        database="cities_weather"
    )

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM weather WHERE city_name = %s", (city_name,))
    city = cursor.fetchone()

    if city:
        city_id = city[0]
        cursor.execute("SELECT temperature, description, time FROM weather WHERE city_id = %s", (city_id,))
        weather = cursor.fetchone()

        if weather:
            print(f"Погода в {city_name}:")
            print(f"Температура: {weather[0]}°C")
            print(f"Описание: {weather[1]}")
            print(f"Время записи: {weather[2]}")
        else:
            print("Погода для этого города ещё не добавлена.")
    else:
        print("Город не найден.")

    connection.close()

city = input("Введите название своего города:\n")
result = weather_api.get_weather(city, 'f666857d5f3ab6a6b27038ec6fcaa706')
try:
    print(result)
    print(f"В городе {result['city']} сейчас {result['temperature']}°C, {result['description']}")
except:
    print(result['error'])


if input("Хочешь найти информацию об определённом городе? Да/Нет\n") == "Да":
    search_weather()