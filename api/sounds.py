import requests
from flask import Blueprint, request, jsonify
import os

sounds_bp = Blueprint('sounds', __name__)

# Конфигурация Яндекс.Диска
YANDEX_OAUTH_TOKEN = "ваш_oauth_токен"  # лучше хранить в переменных окружения
YANDEX_UPLOAD_URL = "https://cloud-api.yandex.net/v1/disk/resources/upload"
YANDEX_DISK_PATH = "/SoundCollab/"  # папка на Яндекс.Диске

@sounds_bp.route('/upload', methods=['POST'])
def upload_sound():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    # Проверка расширения файла
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    # Загрузка файла на Яндекс.Диск
    try:
        # 1. Получаем ссылку для загрузки
        headers = {"Authorization": f"OAuth {YANDEX_OAUTH_TOKEN}"}
        params = {
            "path": f"{YANDEX_DISK_PATH}{file.filename}",
            "overwrite": "true"
        }
        response = requests.get(YANDEX_UPLOAD_URL, headers=headers, params=params)
        response.raise_for_status()
        upload_url = response.json().get("href")

        # 2. Загружаем файл
        with file.stream as f:
            upload_response = requests.put(upload_url, data=f)
            upload_response.raise_for_status()

        return jsonify({
            "status": "success",
            "filename": file.filename,
            "url": f"https://disk.yandex.ru/client/disk{SoundCollab}/{file.filename}",
            "metadata": request.form.get('metadata', {})
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'wav', 'mp3', 'ogg'}
