from flask import Flask, render_template, send_from_directory, request, jsonify, send_file, url_for
from main import generate
import os

app = Flask(__name__)

# Paths to audio directories
MALE_DIR = './mnt/data/male'
FEMALE_DIR = './mnt/data/female'
DATA_DIR = './mnt/data'

@app.route('/')
def index():
    return render_template('index.html', home_active=True)

# Route to serve male audio files
@app.route('/audio/male/<filename>')
def male_audio(filename):
    return send_from_directory(MALE_DIR, filename)

# Route to serve female audio files
@app.route('/audio/female/<filename>')
def female_audio(filename):
    return send_from_directory(FEMALE_DIR, filename)

# Route to handle the "Generate" request
@app.route('/generate-audio', methods=['POST'])
def generate_audio():
    data = request.json
    voice = data.get('voice')
    text = data.get('text')
    gender = data.get('gender')

    # Call the generate function
    try:
        generated_file_path = generate(voice, text, gender)
        download_link = f"/download-audio/{gender}"  # Link for download
        return jsonify(
            {"status": "success", "message": "Audio generated successfully!", "download_link": download_link})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Route to download the generated audio file
@app.route('/download-audio/<gender>')
def download_audio(gender):
    file_path = os.path.join(DATA_DIR, gender, "Audio.wav")
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"status": "error", "message": "File not found!"}), 404

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
