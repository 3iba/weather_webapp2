from flask import Flask, request, render_template, redirect, url_for
import weather_api
import database
app = Flask(__name__)
API_KEY = "f666857d5f3ab6a6b27038ec6fcaa706"


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        city = request.form.get('city')
        result = weather_api.get_weather(city, API_KEY)
    return render_template('index.html', result=result)

@app.route('/about')
def about():
    search = request.args.get('search', '').strip()
    all_data = database.get_weather_table_data()
    if search:
        filtered_data = [row for row in all_data if search.lower() in row['city_name'].lower()]
    else:
        filtered_data = all_data
    return render_template('about.html', table=filtered_data)


@app.route('/delete_city', methods=['POST'])
def delete_city():
    city_name = request.form['city_name']
    database.delete_record(city_name)
    return redirect(url_for('about'))

if __name__ == '__main__':
    app.run(debug=True)

