from flask import Flask

# Flask server (port tələbini təmin etmək üçün)
flask_app = Flask(__name__)

# Flask boş səhifə
@flask_app.route("/")
def index():
    print("🌐 Flask serverinə HTTP sorğusu göndərildi.")
    return "Telegram Bot işləyir! 👌"

if __name__ == "main":
    # Telegram botunu və Flask serverini işə sal
    from threading import Thread

    def run_flask():
        print("🚀 Flask server işə salınır...")
        flask_app.run(host="0.0.0.0", port=8000)

    Thread(target=run_flask).start()
    print("⚙️ Flask server fon rejimində işə salındı.")
    run_pyrogram() # type: ignore
