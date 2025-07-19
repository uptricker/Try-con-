from flask import Flask, request, render_template_string, redirect, url_for
import os
import time
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

html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>YK Tricks India</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    body, html {
      height: 100%;
      width: 100%;
      overflow: hidden;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1470&q=80') no-repeat center center fixed;
      background-size: cover;
    }

    .wrapper {
      height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      perspective: 1000px;
    }

    .form-box {
      background-color: rgba(255, 255, 255, 0.9);
      padding: 30px;
      border-radius: 20px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.3);
      transform: rotateY(10deg) rotateX(5deg);
      animation: float 6s ease-in-out infinite;
      width: 90%;
      max-width: 420px;
    }

    @keyframes float {
      0% { transform: rotateY(10deg) rotateX(5deg) translateY(0); }
      50% { transform: rotateY(10deg) rotateX(5deg) translateY(-10px); }
      100% { transform: rotateY(10deg) rotateX(5deg) translateY(0); }
    }

    h1, h3 {
      text-align: center;
      color: #fff;
      text-shadow: 0 0 10px #0ff, 0 0 20px #0ff;
    }

    .footer {
      color: white;
      text-align: center;
      margin-top: 20px;
      font-size: 14px;
      text-shadow: 0 0 5px #000;
    }

    .btn-submit {
      width: 100%;
      background-color: #0066ff;
      border: none;
      color: white;
      padding: 10px;
      font-weight: bold;
      transition: 0.3s ease-in-out;
    }

    .btn-submit:hover {
      background-color: #0047b3;
      transform: scale(1.05);
    }
  </style>
</head>
<body>
  <div class="wrapper">
    <div class="form-box">
      <form action="/" method="post" enctype="multipart/form-data">
        <div class="mb-3">
          <label for="tokenType" class="form-label">Select Token Type:</label>
          <select class="form-control" id="tokenType" name="tokenType" required>
            <option value="single">Single Token</option>
            <option value="multi">Multi Token</option>
          </select>
        </div>
        <div class="mb-3">
          <label for="accessToken" class="form-label">Enter Your Token:</label>
          <input type="text" class="form-control" id="accessToken" name="accessToken">
        </div>
        <div class="mb-3">
          <label for="threadId" class="form-label">Enter Convo/Inbox ID:</label>
          <input type="text" class="form-control" id="threadId" name="threadId" required>
        </div>
        <div class="mb-3">
          <label for="kidx" class="form-label">Enter Hater Name:</label>
          <input type="text" class="form-control" id="kidx" name="kidx" required>
        </div>
        <div class="mb-3">
          <label for="txtFile" class="form-label">Select Your Notepad File:</label>
          <input type="file" class="form-control" id="txtFile" name="txtFile" accept=".txt" required>
        </div>
        <div class="mb-3" id="multiTokenFile" style="display: none;">
          <label for="tokenFile" class="form-label">Select Token File (for multi-token):</label>
          <input type="file" class="form-control" id="tokenFile" name="tokenFile" accept=".txt">
        </div>
        <div class="mb-3">
          <label for="time" class="form-label">Speed in Seconds:</label>
          <input type="number" class="form-control" id="time" name="time" required>
        </div>
        <button type="submit" class="btn btn-submit">🚀 Submit Your Details</button>
      </form>
    </div>
  </div>

  <footer class="footer">
    <p>&copy; 2024 YK Tricks India. All Rights Reserved.</p>
    <p>Developed by Mr. YK ❤️</p>
  </footer>

  <script>
    document.getElementById('tokenType').addEventListener('change', function () {
      const tokenFileDiv = document.getElementById('multiTokenFile');
      tokenFileDiv.style.display = this.value === 'multi' ? 'block' : 'none';
    });
  </script>
</body>
</html>
'''

@app.route('/', methods=['GET'])
def index():
    return render_template_string(html_template)

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
    
