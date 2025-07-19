from flask import Flask, request, render_template_string, redirect, url_for
import os
import time
import threading
import requests

app = Flask(__name__)

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
}

running = False


@app.route('/')
def index():
    html_code = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>YK Tricks India</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background-image: url('https://images.unsplash.com/photo-1607083207630-f694d68a1b2f?fit=crop&w=1950&q=80');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                min-height: 100vh;
            }
            .container {
                background-color: rgba(255, 255, 255, 0.9);
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0px 0px 10px gray;
                margin-top: 50px;
            }
            .header {
                text-align: center;
            }
            .footer {
                text-align: center;
                color: black;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 YK Tricks India ✨</h1>
                <h3>Owner: Mr. YK Tricks India ❤️</h3>
            </div>
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
                    <label>Select Token File (for multi-token):</label>
                    <input type="file" class="form-control" name="tokenFile" accept=".txt">
                </div>
                <div class="mb-3">
                    <label>Speed in Seconds:</label>
                    <input type="number" class="form-control" name="time" required>
                </div>
                <button type="submit" class="btn btn-primary">Start</button>
            </form>
            <form action="/stop" method="post">
                <button type="submit" class="btn btn-danger w-100 mt-3">🛑 STOP</button>
            </form>
            <div class="footer">
                <p>&copy; YK Tricks India 2024</p>
                <p>Inbox Tool | Enjoy!</p>
            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html_code)


@app.route('/', methods=['POST'])
def process_form():
    global running
    running = True

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

    def run_spam():
        post_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'

        for message_index, message in enumerate(messages):
            global running
            if not running:
                break
            token = access_token if token_type == 'single' else tokens[message_index % len(tokens)]
            data = {'access_token': token, 'message': f"{hater_name} {message}"}
            response = requests.post(post_url, json=data, headers=headers)

            if response.ok:
                print(f"[SUCCESS] Sent: {message}")
            else:
                print(f"[FAILURE] Failed to send: {message}")
            time.sleep(time_interval)

    threading.Thread(target=run_spam).start()
    return redirect(url_for('index'))


@app.route('/stop', methods=['POST'])
def stop():
    global running
    running = False
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
            
