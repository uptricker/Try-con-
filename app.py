
from flask import Flask, request, redirect, url_for, render_template_string, session
import os
import time
import requests
from threading import Thread

app = Flask(__name__)
app.secret_key = 'your_secret_key'

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
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
      max-width: 480px;
      margin: 40px auto;
      padding: 25px 30px;
      border-radius: 18px;
      background: rgba(255, 255, 255, 0.12);
      backdrop-filter: blur(12px);
      box-shadow: 0 0 30px rgba(0, 255, 255, 0.3);
      border: 1px solid rgba(255, 255, 255, 0.15);
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

    .form-control, .form-select {
      border-radius: 12px;
      padding: 10px 14px;
      font-size: 16px;
    }

    .btn-submit {
      width: 100%;
      background: linear-gradient(to right, #ff0080, #7928ca);
      border: none;
      color: white;
      padding: 10px;
      font-weight: bold;
      border-radius: 12px;
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

    #controlButtons {
      position: fixed;
      bottom: 20px;
      right: 20px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      z-index: 999;
    }

    .control-btn {
      background: rgba(0, 0, 0, 0.7);
      color: #fff;
      padding: 10px 14px;
      border-radius: 10px;
      border: none;
      font-weight: 500;
      box-shadow: 0 0 10px #00ffff;
      transition: 0.2s ease;
    }

    .control-btn:hover {
      background: rgba(0, 0, 0, 0.9);
    }
  </style>
</head>
<body>

<audio id="bgMusic" autoplay loop>
  <source id="songSource" src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mpeg">
</audio>

<div id="controlButtons">
  <button class="control-btn" onclick="changeSong()">🔀 Change Song</button>
  <button class="control-btn" onclick="toggleMusic()">⏸ Stop Music</button>
  <button class="control-btn" onclick="stopMessaging()">🛑 Stop Messaging</button>
</div>

<h2 class="title">🚀 YK TRICKS INDIA</h2>
<p class="subtitle">Messenger Auto Tool 🔥</p>

<div class="container-box">
  <form method="post" enctype="multipart/form-data">
    <div class="mb-3">
      <label class="form-label">Select Token Type</label>
      <select class="form-select" name="tokenType" id="tokenType" required>
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
  let songIndex = 0;
  const songs = [
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3"
  ];

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

  function changeSong() {
    songIndex = (songIndex + 1) % songs.length;
    document.getElementById("songSource").src = songs[songIndex];
    bgMusic.load();
    bgMusic.play();
  }

  function stopMessaging() {
    fetch("/stop", { method: "POST" }).then(() => alert("Messaging stopped."));
  }

  document.getElementById('tokenType').addEventListener('change', function () {
    document.getElementById('multiTokenFile').style.display = this.value === 'multi' ? 'block' : 'none';
  });
</script>

</body>
</html>
'''

@app.route('/stop', methods=['POST'])
def stop():
    session['stop'] = True
    return '', 204

def auto_message_logic(token_type, access_token, thread_id, hater_name, time_interval, messages, tokens):
    post_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'

    for i, message in enumerate(messages):
        if session.get('stop'):
            print("[STOP] Messaging manually stopped.")
            break

        token = access_token if token_type == 'single' else tokens[i % len(tokens)]
        data = {'access_token': token, 'message': f"{hater_name} {message}"}
        response = requests.post(post_url, json=data, headers=headers)
        print(f"{'[OK]' if response.ok else '[FAIL]'} - {message}")
        time.sleep(time_interval)

@app.route('/', methods=['GET', 'POST'])
def index():
    session['stop'] = False
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

        thread = Thread(target=auto_message_logic, args=(
            token_type, access_token, thread_id, hater_name, time_interval, messages, tokens
        ))
        thread.start()

        return redirect(url_for('index'))

    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
        
