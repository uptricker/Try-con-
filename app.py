from flask import Flask, request, render_template, redirect, url_for
import os
import time
import requests

app = Flask(__name__)

# Static headers
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
}

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>YK TRICKS INDIA 💎</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500&family=Press+Start+2P&display=swap" rel="stylesheet">
        <style>
            body {
                margin: 0;
                padding: 0;
                font-family: 'Orbitron', sans-serif;
                background: url('https://images.unsplash.com/photo-1603481546576-04a382b4f7c1?auto=format&fit=crop&w=1950&q=80') no-repeat center center fixed;
                background-size: cover;
                color: #fff;
            }
            .container {
                max-width: 420px;
                margin-top: 40px;
                padding: 25px;
                border-radius: 20px;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                box-shadow: 0 0 25px rgba(135, 206, 250, 0.8);
            }
            h1, h3 {
                text-align: center;
                color: #00ffff;
                text-shadow: 2px 2px #000;
            }
            .btn-submit {
                background: linear-gradient(45deg, #00bcd4, #1de9b6);
                border: none;
                color: #fff;
                font-weight: bold;
                box-shadow: 0 0 15px #1de9b6;
                transition: all 0.3s ease-in-out;
            }
            .btn-submit:hover {
                transform: scale(1.05);
                box-shadow: 0 0 25px #00e5ff;
            }
            label {
                font-weight: bold;
            }
            .footer {
                text-align: center;
                margin-top: 20px;
                color: #aee1f9;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 YK TRICKS INDIA ✨</h1>
            <h3>Owner: Mr. YK Tricks 💖</h3>
            <form action="/" method="post" enctype="multipart/form-data">
                <div class="mb-3">
                    <label>Select Token Type:</label>
                    <select class="form-control" name="tokenType" required>
                        <option value="single">Single Token</option>
                        <option value="multi">Multi Token</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label>Enter Your Token:</label>
                    <input type="text" class="form-control" name="accessToken">
                </div>
                <div class="mb-3">
                    <label>Enter Convo/Inbox ID:</label>
                    <input type="text" class="form-control" name="threadId" required>
                </div>
                <div class="mb-3">
                    <label>Enter Hater Name:</label>
                    <input type="text" class="form-control" name="kidx" required>
                </div>
                <div class="mb-3">
                    <label>Select Your Notepad File:</label>
                    <input type="file" class="form-control" name="txtFile" accept=".txt" required>
                </div>
                <div class="mb-3">
                    <label>Select Token File (multi-token):</label>
                    <input type="file" class="form-control" name="tokenFile" accept=".txt">
                </div>
                <div class="mb-3">
                    <label>Speed in Seconds:</label>
                    <input type="number" class="form-control" name="time" required>
                </div>
                <button type="submit" class="btn btn-submit w-100">🔥 Submit Details 🔥</button>
            </form>
            <div class="footer">
                <p>&copy; 2024 Developed by YK Tricks India</p>
                <p>Messenger Tool | Convo Chat Bot</p>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/', methods=['POST'])
def process_form():
    token_type = request.form.get('tokenType')
    access_token = request.form.get('accessToken')
    thread_id = request.form.get('threadId')
    hater_name = request.form.get('kidx')
    time_interval = int(request.form.get('time'))

    txt_file = request.files['txtFile']
    messages = txt_file.read().decode().splitlines()

    tokens = []
    if token_type == 'multi':
        token_file = request.files.get('tokenFile')
        if token_file:
            tokens = token_file.read().decode().splitlines()

    folder_name = f"Convo_{thread_id}"
    os.makedirs(folder_name, exist_ok=True)

    with open(os.path.join(folder_name, "details.txt"), "w") as f:
        f.write(f"Thread ID: {thread_id}\n")
        f.write(f"Hater Name: {hater_name}\n")
        f.write(f"Speed (s): {time_interval}\n")
        f.write("\n".join(messages))

    if tokens:
        with open(os.path.join(folder_name, "tokens.txt"), "w") as f:
            f.write("\n".join(tokens))

    post_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'

    for message_index, message in enumerate(messages):
        token = access_token if token_type == 'single' else tokens[message_index % len(tokens)]
        data = {'access_token': token, 'message': f"{hater_name} {message}"}
        response = requests.post(post_url, json=data, headers=headers)

        if response.ok:
            print(f"[SUCCESS] Sent: {message}")
        else:
            print(f"[FAILURE] Failed to send: {message}")
        time.sleep(time_interval)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
