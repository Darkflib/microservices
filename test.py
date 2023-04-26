import requests
import mimetypes

# Replace 'your_code' with the code you want to highlight
your_code = """
def hello_world():
    print("Hello, World!")
"""

payload = {
    "code": your_code,
    # Optional: specify the language (e.g., "python", "javascript", "html", etc.)
    "language": "python",
    # Optional: specify the output format (e.g., "html", "latex", "bbcode", "png", etc.)
    "format": "html",
    # Optional: set 'download' to True to download the formatted code as a file
    "download": True
}

response = requests.post("http://127.0.0.1:8000/highlight", json=payload)

if response.status_code == 200:
    extension = mimetypes.guess_extension(response.headers["Content-Type"])
    file_name = f"highlighted_code{extension}"
    
    with open(file_name, 'wb') as f:
        f.write(response.content)
    print(f"File saved as {file_name}")
else:
    print(f"Error: {response.status_code}")

