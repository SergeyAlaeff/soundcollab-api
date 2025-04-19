from flask import Blueprint, request, jsonify
import os

sounds_bp = Blueprint('sounds', __name__)

@sounds_bp.route('/upload', methods=['POST'])
def upload_sound():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    # Сохраняем файл временно (в продакшене используйте S3)
    os.makedirs('uploads', exist_ok=True)
    file.save(f"uploads/{file.filename}")

    return jsonify({
        "status": "success",
        "filename": file.filename,
        "metadata": request.form.get('metadata', {})
    })

@sounds_bp.route('/search', methods=['GET'])
def search_sounds():
    query = request.args.get('q', '')
    # Здесь должна быть логика поиска (пока заглушка)
    return jsonify({"results": [], "query": query})
