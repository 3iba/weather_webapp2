import mysql.connector
from datetime import datetime
import logging
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def databaseConnect(city_name, country, temperature, description):
    if not isinstance(temperature, (int, float)):
        raise ValueError("Температура должна быть числом")
    if not city_name or not country or not description:
        raise ValueError("Поля 'city_name', 'country' и 'description' не должны быть пустыми")
    if temperature < -60:
        raise ValueError("Превышена минимальная температура")
    if temperature > 60:
        raise ValueError("Превышена максимальная температура")

    try:
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")

        connection = mysql.connector.connect(
            host="MySQL-8.2",
            user="root",
            password="",
            database="cities_weather"
        )

        cursor = connection.cursor()

        cursor.execute("SELECT id FROM cities WHERE city_name = %s", (city_name,))
        result = cursor.fetchone()

        if result:
            city_id = result[0]
        else:
            cursor.execute("INSERT INTO cities (city_name, country) VALUES (%s, %s)", (city_name, country))
            connection.commit()
            city_id = cursor.lastrowid

        cursor.execute("SELECT id FROM weather WHERE city_id = %s", (city_id,))
        weather_result = cursor.fetchone()

        if weather_result:
            cursor.execute(
                "UPDATE weather SET temperature = %s, description = %s, weather_time = %s WHERE city_id = %s",
                (temperature, description, time_str, city_id)
            )
        else:
            cursor.execute(
                "INSERT INTO weather (city_id, temperature, description, weather_time) VALUES (%s, %s, %s, %s)",
                (city_id, temperature, description, time_str)
            )

        connection.commit()
        connection.close()
    except Exception as e:
        logging.error(f"Ошибка при сохранении данных о городе {city_name}: {e}")
        with open('error.log', 'a') as f:
            f.write(f"Ошибка при сохранении данных о городе {city_name}: {e}\n")



def get_weather_table_data():
    connection = mysql.connector.connect(
        host="MySQL-8.2",
        user="root",
        password="",
        database="cities_weather"
    )

    cursor = connection.cursor(dictionary=True)

    cursor.execute('''
        SELECT c.city_name, c.country, w.temperature, w.description, w.weather_time
        FROM cities c
        JOIN weather w ON c.id = w.city_id
    ''')

    result = cursor.fetchall()

    connection.close()
    return result


def delete_record(city_name):
    connection = mysql.connector.connect(
        host="MySQL-8.2",
        user="root",
        password="",
        database="cities_weather"
    )
    cursor = connection.cursor()


    cursor.execute('DELETE FROM weather WHERE city_id = (SELECT id FROM cities WHERE city_name = %s)', (city_name,))


    cursor.execute('DELETE FROM cities WHERE city_name = %s', (city_name,))
    
    connection.commit()
    connection.close()
