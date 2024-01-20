import logging
from flask import Flask, request, render_template_string
import json
import base58

app = Flask(__name__)

# Set log level to ERROR to minimize logging output
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/', methods=['GET', 'POST'])
def index():
    encoded_key = ''
    error_message = ''

    if request.method == 'POST':
        json_data = request.form['json_data']
        try:
            wallet_data = json.loads(json_data)
            # Convert the private key to bytes and encode using base58
            encoded_key = base58.b58encode(bytes(wallet_data)).decode('utf-8')
        except Exception as e:
            error_message = f"An error occurred: {e}"

    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Wallet Key Encoder</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    background-color: #f2f2f2;
                }
                .container {
                    width: 50%;
                    max-width: 600px;
                    padding: 20px;
                    background: white;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }
                textarea {
                    width: 100%;
                    height: 100px;
                    margin-bottom: 10px;
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    resize: vertical;
                }
                input[type="submit"] {
                    width: 100%;
                    padding: 10px;
                    border: none;
                    border-radius: 5px;
                    background-color: #4CAF50;
                    color: white;
                    font-size: 16px;
                    cursor: pointer;
                }
                input[type="submit"]:hover {
                    background-color: #45a049;
                }
                .output {
                    margin-top: 20px;
                    word-wrap: break-word;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Wallet Key Encoder</h1>
                <form method="post">
                    <textarea name="json_data" placeholder="Paste JSON content here"></textarea>
                    <input type="submit" value="Encode and Display">
                </form>
                {% if encoded_key %}
                    <div class="output">Encoded Private Key: {{ encoded_key }}</div>
                {% endif %}
                {% if error_message %}
                    <div class="output">{{ error_message }}</div>
                {% endif %}
            </div>
        </body>
        </html>
        ''', encoded_key=encoded_key, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
