from flask import Flask, request, redirect, url_for, render_template_string
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
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>YK Tricks India</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" />
  <style>
    body, html {
      margin: 0;
      padding: 0;
      height: 100%;
      font-family: 'Segoe UI', sans-serif;
      background: #0d0d0d;
      overflow-x: hidden;
    }

    body::before {
      content: '';
      position: fixed;
      top: 0; left: 0;
      width: 100%; height: 100%;
      background: url('https://i.ibb.co/0j1YBtd/rain-overlay.gif') repeat;
      background-size: cover;
      opacity: 0.25;
      z-index: -1;
    }

    .container-box {
      max-width: 500px;
      margin: auto;
      background-color: rgba(255,255,255,0.95);
      padding: 30px;
      margin-top: 50px;
      border-radius: 20px;
      box-shadow: 0 0 25px rgba(0,255,255,0.3);
    }

    .title {
      text-align: center;
      color: #ffffff;
      text-shadow: 0 0 12px #00ffff;
      font-size: 28px;
      margin-top: 20px;
    }

    .subtitle {
      text-align: center;
      color: #ffffff;
      font-size: 16px;
      margin-bottom: 20px;
    }

    .form-label {
      font-weight: bold;
    }

    .btn-submit {
      width: 100%;
      background: linear-gradient(to right, #ff0080, #7928ca);
      border: none;
      color: white;
      padding: 10px;
      font-weight: bold;
      transition: 0.3s ease-in-out;
    }

    .btn-submit:hover {
      transform: scale(1.05);
      box-shadow: 0 0 10px #00ffff;
    }

    .footer {
      color: white;
      text-align: center;
      margin-top: 40px;
      margin-bottom: 20px;
      font-size: 14px;
    }

    #musicControl {
      position: fixed;
      bottom: 20px;
      right: 20px;
      background-color: rgba(0,0,0,0.7);
      color: white;
      border: none;
      padding: 10px 16px;
      border-radius: 8px;
      cursor: pointer;
      z-index: 1000;
      box-shadow: 0 0 12px #00ffff;
    }

    #musicControl:hover {
      background-color: rgba(0,0,0,0.9);
    }
  </style>
</head>
<body>

<audio id="bgMusic" autoplay loop>
  <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mpeg">
</audio>
<button id="musicControl" onclick="toggleMusic()">⏸ Stop Music</button>

<h2 class="title">🚀 YK TRICKS INDIA</h2>
<p class="subtitle">Messenger Auto Tool 🔥</p>

<div class="container-box">
  <form method="post" enctype="multipart/form-data">
    <div class="mb-3">
      <label class="form-label">Select Token Type</label>
      <select class="form-control" name="tokenType" id="tokenType" required>
        <option value="single">Single Token</option>
        <option value="multi">Multi Token</option>
      </select>
    </div>
    <div class="mb-3">
      <label class="form-label">Enter Your Token</label>
      <input type="text" class="form-control" name="accessToken">
    </div>
    <div class="mb-3">
      <label class="form-label">Enter Thread/Inbox ID</label>
      <input type="text" class="form-control" name="threadId" required>
    </div>
    <div class="mb-3">
      <label class="form-label">Enter Hater Name</label>
      <input type="text" class="form-control" name="kidx" required>
    </div>
    <div class="mb-3">
      <label class="form-label">Upload Message File (.txt)</label>
      <input type="file" class="form-control" name="txtFile" accept=".txt" required>
    </div>
    <div class="mb-3" id="multiTokenFile" style="display: none;">
      <label class="form-label">Multi Token File (.txt)</label>
      <input type="file" class="form-control" name="tokenFile" accept=".txt">
    </div>
    <div class="mb-3">
      <label class="form-label">Delay (in seconds)</label>
      <input type="number" class="form-control" name="time" required>
    </div>
    <button type="submit" class="btn btn-submit">💬 Start Auto Messaging</button>
  </form>
</div>

<div class="footer">
  &copy; 2024 - YK Tricks India | All Rights Reserved 🌐<br>
  Telegram: @yktricksindia
</div>

<script>
  const bgMusic = document.getElementById("bgMusic");
  const musicControl = document.getElementById("musicControl");
  let isPlaying = true;

  function toggleMusic() {
    if (isPlaying) {
      bgMusic.pause();
      musicControl.textContent = "▶ Play Music";
    } else {
      bgMusic.play();
      musicControl.textContent = "⏸ Stop Music";
    }
    isPlaying = !isPlaying;
  }

  document.getElementById('tokenType').addEventListener('change', function () {
    document.getElementById('multiTokenFile').style.display = this.value === 'multi' ? 'block' : 'none';
  });
</script>

</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
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

        for i, message in enumerate(messages):
            token = access_token if token_type == 'single' else tokens[i % len(tokens)]
            data = {'access_token': token, 'message': f"{hater_name} {message}"}
            response = requests.post(post_url, json=data, headers=headers)
            print(f"{'[OK]' if response.ok else '[FAIL]'} - {message}")
            time.sleep(time_interval)

        return redirect(url_for('index'))

    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
                      
