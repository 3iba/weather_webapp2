import requests
import database
import logging

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)



logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(message)s', encoding='utf=8')

logger = logging.getLogger(__name__)

def get_weather(city: str, api_key: str) -> dict:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
    try:
        r = requests.get(url)
        a = r.json()
    except Exception as e:
        logger.error(f"Ошибка сети при запросе погоды для города {city}: {e}")
        return {"error": "Ошибка сети"}

    if str(a['cod']) == '401':
        logger.error(f"Неверный API-ключ при запросе для города {city}")
        return {"error": "Ошибка! Неверный API-ключ"}

    if str(a['cod']) == '404':
        logger.error(f"Неверное название города: {city}")
        return {"error": "Ошибка! Неверное название города"}

    database.databaseConnect(a['name'], a['sys']['country'], a['main']['temp'], a['weather'][0]['description'].capitalize())
    return {"city": a['name'], "temperature": a['main']['temp'], "description": a['weather'][0]['description'].capitalize()}
# get_weather("Astana", "f666857d5f3ab6a6b27038ec6fcaa706")