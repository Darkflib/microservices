from flask import Flask, request, jsonify, send_file
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import get_formatter_by_name, ImageFormatter
from io import BytesIO
import mimetypes

app = Flask(__name__)

@app.route('/highlight', methods=['POST'])
def colorize_code():
    # Get input data from the POST request
    data = request.get_json()
    code = data.get('code', '')
    language = data.get('language', '')
    output_format = data.get('format', 'html')
    download = data.get('download', False)

    # Determine the appropriate lexer based on language or guess it
    if language:
        lexer = get_lexer_by_name(language)
    else:
        lexer = guess_lexer(code)

    # Determine the appropriate formatter based on output_format
    formatter = get_formatter_by_name(output_format)

    # Colorize the code and convert it to the desired format
    formatted_code = highlight(code, lexer, formatter)

#    # If the download option is set, send the formatted code as a file
#    if download:
#        file_extension = formatter.filename_extensions[0] if formatter.filename_extensions else ""
#        filename = f"highlighted_code{file_extension}"
#        mime_type, _ = mimetypes.guess_type(filename)
#
#        if isinstance(formatter, ImageFormatter):
#            img_io = BytesIO()
#            img_io.write(formatted_code)
#            img_io.seek(0)
#            return send_file(img_io, mimetype=mime_type, as_attachment=True, attachment_filename=filename)
#        else:
#            text_io = BytesIO(formatted_code.encode())
#            return send_file(text_io, mimetype=mime_type, as_attachment=True, attachment_filename=filename)
#
    # For other cases, return the highlighted code as JSON
    return jsonify({"formatted_code": formatted_code})

if __name__ == '__main__':
    app.run()