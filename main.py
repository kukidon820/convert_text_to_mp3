import os
from flask import Flask, render_template, request, send_from_directory, jsonify
from translate_text_to_mp3 import pdf_to_mp3
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

AUDIO_DIR = os.getenv('AUDIO_DIR', 'audio/')
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'files/')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route("/", methods=['GET', 'POST'])
def make_mp3():
    if request.method == 'POST':

        for i in [AUDIO_DIR, UPLOAD_FOLDER]:
            for file in os.listdir(i):
                file_path = os.path.join(i, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)

        f = request.files['file']
        lan = request.form.get('language')
        print(f"Получил файл - {f.filename}")

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)

        print(f"Путь для сохранения - {file_path}")

        with open(file_path, "wb") as file:
            file.write(f.read())

        file_mp3 = pdf_to_mp3(file_path, lan, AUDIO_DIR)
        print("Получил последний файл!")

        if file_mp3:
            print("успешно сделал")
            return jsonify({"success": True, "filename": file_mp3})

        return jsonify({"success": False})

    return render_template("index.html")


@app.route('/download/<filename>', methods=['POST'])
def download_mp3(filename):
    return send_from_directory('audio', filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
