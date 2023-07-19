from flask import Flask, request, send_file, jsonify
import os
import subprocess
import tempfile
import logging
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)
# add logging to console, with level set by optional env var
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

def convert_mmd_to_img(mmd_filename, img_filename, img_format, theme, width, height, bg_color, scale):
    # convert mmd to img
    cmd = [
        'mmdc',
        '-i', mmd_filename,
        '-o', img_filename,
        '-t', theme,
        '-w', str(width),
        '-H', str(height),
        '-b', bg_color,
        '-s', str(scale)
    ]

    if img_format == 'svg':
        cmd.append('--svg')

    logging.info(f"cmd: {cmd}")
    subprocess.run(cmd, check=True)

@app.route('/render-mermaid', methods=['POST'])
def render_mermaid():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON input."}), 400

    graph_definition = data.get('graph_definition')
    img_format = data.get('img_format', 'png').lower()
    theme = data.get('theme', 'default')
    width = min(data.get('width', 800), 2048)
    height = min(data.get('height', 600), 2048)
    bg_color = data.get('bg_color', 'transparent')
    scale = data.get('scale', 1)
    # log request data
    logging.info(f"graph_definition: {graph_definition}")
    logging.info(f"img_format: {img_format}")
    logging.info(f"theme: {theme}")
    logging.info(f"width: {width}")
    logging.info(f"height: {height}")
    logging.info(f"bg_color: {bg_color}")
    logging.info(f"scale: {scale}")

    if not graph_definition:
        return jsonify({"error": "graph_definition is required."}), 400

    if img_format not in ['png', 'svg']:
        return jsonify({"error": "Invalid image format. Accepted formats are png and svg."}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{img_format}') as f:
        temp_filename = f.name

    with tempfile.NamedTemporaryFile(delete=False, suffix='.mmd') as f:
        f.write(graph_definition.encode())
        mmd_filename = f.name

    # try to convert mmd to svg
    try:
        convert_mmd_to_img(mmd_filename, temp_filename, img_format, theme, width, height, bg_color, scale)
    except Exception as e:
        # remove temp files
        os.remove(temp_filename)
        os.remove(mmd_filename)
        return jsonify({"error": f"Error rendering mermaid graph: {e}"}), 500
    
    os.remove(mmd_filename)

    result = send_file(temp_filename, mimetype=f'image/{img_format}')

    return result

if __name__ == '__main__':
    app.run()
