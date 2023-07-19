import os
import subprocess
from flask import Flask, request, send_file

app = Flask(__name__)

def synthesize_speech(text, output_filename):
    cmd = f"pico2wave -w {output_filename} '{text}'"
    subprocess.run(cmd, shell=True, check=True)

@app.route('/synthesize', methods=['POST'])
def synthesize():
    text = request.form.get('text')
    if text is None:
        return {"error": "No text provided"}, 400

    output_filename = "output.wav"
    synthesize_speech(text, output_filename)

    return send_file(output_filename, mimetype='audio/wav')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)