"""tts api using native apple tts

Usage:
    python app.py

    curl -X POST -F 'text=hello world' http://localhost:5000/synthesize > output.wav

"""


import os
import subprocess
from flask import Flask, request, send_file
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# use apple native tts
def synthesize_speech(text, output_filename):
    # create aiff file with text from input
    try:
        cmd = ['say', '-v', 'Ava (Enhanced)', '-o', output_filename + '.aiff', text]
    
        # run the command and wait for it to finish, log output and errors
        logging.debug("Running command: %s", cmd)
        # get return code and capture output, raise exception if it is not 0, and display the error
        return_code = subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        logging.error("Error running command: %s", e.stderr)
        raise e
    logging.debug("Return code: %s", return_code.returncode)
    logging.debug("Output: %s", return_code.stdout)
    logging.debug("Error: %s", return_code.stderr)
    

    # convert aiff to wav
    cmd = ['sox', output_filename + '.aiff', output_filename + '.wav']
    logging.debug("Running command: %s", cmd)
    subprocess.run(cmd, check=True)


@app.route('/synthesize', methods=['POST'])
def synthesize():
    text = request.form.get('text')
    if text is None:
        return {"error": "No text provided"}, 400

    # get current working directory
    cwd = os.getcwd()
    # create output filename
    output_filename = os.path.join(cwd, 'output')
    # synthesize speech
    synthesize_speech(text, output_filename)
    # send_file will automatically delete the file after sending it to the client (default behavior)
    return send_file(output_filename + '.wav', mimetype='audio/wav')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
