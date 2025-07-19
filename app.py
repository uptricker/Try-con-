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

# 🖼️ HTML Template with all visual effects
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>YK Tricks India</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" />
  <style>
    html, body {
      margin: 0;
      padding: 0;
      height: 100%;
      background: #0e0e0e;
      overflow: hidden;
      font-family: 'Segoe UI', sans-serif;
    }

    body::before {
      content: '';
      position: fixed;
      top: 0; left: 0;
      width: 100%; height: 100%;
      background: url('https://i.ibb.co/0j1YBtd/rain-overlay.gif') repeat;
      background-size: cover;
      z-index: -2;
      opacity: 0.4;
    }

    body::after {
      content: '';
      position: fixed;
      top: 0; left: 0;
      width: 100%; height: 100%;
      background: url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1470&q=80') no-repeat center center fixed;
      background-size: cover;
      filter: blur(3px) brightness(0.4);
      z-index: -3;
    }

    .wrapper {
      height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      perspective: 1000px;
    }

    .form-box {
      background-color: rgba(255, 255, 255, 0.95);
      padding: 30px;
      border-radius: 20px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.3);
      transform: rotateY(8deg) rotateX(3deg);
      animation: float 6s ease-in-out infinite;
      width: 90%;
      max-width: 420px;
      z-index: 1;
    }

    @keyframes float {
      0%, 100% { transform: rotateY(8deg) rotateX(3deg) translateY(0); }
      50% { transform: rotateY(8deg) rotateX(3deg) translateY(-10px); }
    }

    h1, h3 {
      text-align: center;
      color: #ffffff;
      text-shadow: 0 0 15px cyan;
      margin-bottom: 20px;
    }

    .footer {
      color: white;
      text-align: center;
      position: absolute;
      bottom: 10px;
      width: 100%;
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

    #musicControl {
      position: fixed;
      bottom: 20px;
      right: 20px;
      background-color: rgba(0,0,0,0.7);
      color: white;
      border: none;
      padding: 10px 18px;
      border-radius: 8px;
      cursor: pointer;
      z-index: 9999;
      box-shadow: 0 0 10px cyan;
    }

    #musicControl:hover {
      background-color: rgba(0,0,0,0.9);
    }
  </style>
</head>
<body>

  <!-- 🎵 Background Music -->
  <audio id="bgMusic" autoplay loop>
    <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mpeg">
    Your browser does not support the audio element.
  </audio>

  <!-- 🎧 Music Control Button -->
  <button id="musicControl" onclick="toggleMusic()">⏸ Stop Music</button>

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
