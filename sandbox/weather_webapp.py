from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

def get_weather(city: str, api_key: str) -> dict:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()
        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"].capitalize()
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

API_KEY = "f666857d5f3ab6a6b27038ec6fcaa706"

TEMPLATE = '''
<form method="post">
  <input name="city" placeholder="Введите город">
  <button type="submit">Получить погоду</button>
</form>

{% if result %}
  {% if result.error %}
    <p style="color: red">{{ result.error }}</p>
  {% else %}
    <p>Город: {{ result.city }}</p>
    <p>Температура: {{ result.temperature }}°C</p>
    <p>Погода: {{ result.description }}</p>
  {% endif %}
{% endif %}
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        city = request.form.get('city')
        result = get_weather(city, API_KEY)
    return render_template_string(TEMPLATE, result=result)
if __name__ == '__main__':
    app.run(debug=True)