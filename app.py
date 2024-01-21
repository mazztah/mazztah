from flask import Flask, render_template, request
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# NASA APOD API-URL
apod_url = "https://api.nasa.gov/planetary/apod"

# Ihr NASA API-Schlüssel hier
api_key = "ReNBTlao6IfTYLc4Uu27j0IujL7l1N1bNcjeVnDf"

@app.route('/', methods=['GET', 'POST'])
def index():
    date = None

    if request.method == 'POST':
        date = request.form.get('date')
        if date:
            # API-Anfrage an die NASA APOD API senden
            params = {'api_key': api_key, 'date': date}
            response = requests.get(apod_url, params=params)

            if response.status_code == 200:
                data = response.json()
                return render_template('search_result.html', data=data)
            else:
                return "Fehler beim Abrufen der Daten von der NASA APOD API."

    # Bild des Tages abrufen
    today = datetime.now()
    params = {'api_key': api_key, 'date': today.strftime('%Y-%m-%d')}
    response = requests.get(apod_url, params=params)

    if response.status_code == 200:
        data_today = response.json()
    else:
        data_today = None

    # Bild von gestern abrufen
    yesterday = today - timedelta(days=1)
    params['date'] = yesterday.strftime('%Y-%m-%d')
    response = requests.get(apod_url, params=params)

    if response.status_code == 200:
        data_yesterday = response.json()
    else:
        data_yesterday = None

    # Bild von vorgestern abrufen
    day_before_yesterday = yesterday - timedelta(days=1)
    params['date'] = day_before_yesterday.strftime('%Y-%m-%d')
    response = requests.get(apod_url, params=params)

    if response.status_code == 200:
        data_day_before_yesterday = response.json()
    else:
        data_day_before_yesterday = None

    return render_template('index.html', date=date, data_today=data_today, data_yesterday=data_yesterday, data_day_before_yesterday=data_day_before_yesterday)

if __name__ == '__main__':
    app.run(debug=True)

