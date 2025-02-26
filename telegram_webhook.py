from flask import Flask, request
import requests

TOKEN = "7744302358:AAE3oF9kCMDh5ZM4RlNN2yYlFcLx61b7zNE"
RASA_URL = "https://api.telegram.org/bot7744302358:AAE3oF9kCMDh5ZM4RlNN2yYlFcLx61b7zNE/setWebhook?url=https://2615-190-2-155-231.ngrok-free.app/webhooks/telegram/webhook"

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    data = request.get_json()
    
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_message = data["message"]["text"]

        # إرسال الرسالة إلى Rasa
        rasa_response = requests.post(RASA_URL, json={"sender": str(chat_id), "message": user_message})
        
        bot_responses = rasa_response.json()
        for response in bot_responses:
            send_message(chat_id, response["text"])

    return "ok"

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(port=5002, debug=True)
