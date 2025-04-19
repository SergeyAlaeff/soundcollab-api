from flask import Flask
from .sounds import sounds_bp

app = Flask(__name__)
app.register_blueprint(sounds_bp, url_prefix='/sounds')

@app.route('/')
def home():
    return "SoundCollab API is running!"
