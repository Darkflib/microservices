from flask import Flask, request, jsonify
import markdown

app = Flask(__name__)

@app.route('/markdown-to-html', methods=['POST'])
def markdown_to_html():
    data = request.get_json()
    markdown_text = data.get('markdown_text', '')

    if not markdown_text:
        return jsonify({'error': 'No markdown_text provided'}), 400

    html = markdown.markdown(markdown_text)
    return jsonify({'html': html})

if __name__ == '__main__':
    app.run()