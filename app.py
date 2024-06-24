from flask import Flask, request, render_template
import requests
import os

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TOKEN}/'

app = Flask(__name__)

def send_message(chat_id, text, method="sendPhoto"):
    url = TELEGRAM_API_URL + method
    if method=="sendPhoto":
        payload = {
            'chat_id': chat_id,
            'photo': text
        }
    else:
       payload = {
            'chat_id': chat_id,
            'text': text
        }     
    requests.post(url, json=payload)

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.json

    if 'message' in update:
        chat_id = update['message']['chat']['id']
        text = update['message']['text']
        method = "sendPhoto"
        if text=="/start":
            text = "Welcome User"
            method = "sendMessage"
        elif text.startswith("/"):
            text = "Invalid url!"
            method = "sendMessage"
        send_message(chat_id, text, method)

    return 'OK'

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5000)
