import os
from dotenv import load_dotenv
from flask import Flask
from routes.chat import chat_bp

load_dotenv()

PORT = int(os.getenv("FLASK_PORT", 8000))

app = Flask(__name__)
app.register_blueprint(chat_bp)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=PORT)