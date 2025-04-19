import requests

def get_weather(city: str, api_key: str) -> dict:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()
        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"]
        }
    except requests.exceptions.HTTPError:
        if r.status_code == 401:
            return {"error": "Неверный API-ключ"}
        elif r.status_code == 404:
            return {"error": "Город не найден"}
        else:
            return {"error": f"HTTP ошибка: {r.status_code}"}
    except requests.exceptions.RequestException:
        return {"error": "Ошибка сети"}