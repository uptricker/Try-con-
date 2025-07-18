from flask import Flask, request, render_template_string, flash, redirect, url_for
from instagrapi import Client
import time
import threading
import os

# Flask setup
app = Flask(__name__)
app.secret_key = "your_secret_key"
stop_flag = False

# HTML UI (3D style + background)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Instagram Inbox Sender</title>
  <style>
    body {
      margin: 0;
      font-family: 'Segoe UI', sans-serif;
      background: url('https://wallpaperaccess.com/full/17450.jpg') no-repeat center center fixed;
      background-size: cover;
      color: white;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }
    .container {
      background: rgba(0,0,0,0.85);
      padding: 40px;
      border-radius: 20px;
      width: 90%%;
      max-width: 500px;
      box-shadow: 0 0 40px cyan;
      backdrop-filter: blur(10px);
    }
    h1 {
      text-align: center;
      font-size: 24px;
      background: linear-gradient(to right, #00ffff, #00bfff);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 20px;
    }
    label {
      font-weight: bold;
      display: block;
      margin-top: 15px;
    }
    input {
      width: 100%%;
      padding: 10px;
      margin-top: 5px;
      border-radius: 10px;
      border: none;
      background: rgba(255,255,255,0.1);
      color: white;
    }
    input[type="file"] {
      background: none;
      border: 1px solid #ccc;
    }
    button {
      margin-top: 20px;
      padding: 12px;
      width: 100%%;
      border: none;
      border-radius: 10px;
      background: linear-gradient(45deg, #00e1ff, #00bfff);
      color: black;
      font-weight: bold;
      box-shadow: 0 10px 20px rgba(0,255,255,0.5);
      transition: all 0.3s ease;
      cursor: pointer;
    }
    button:hover {
      transform: scale(1.05);
      box-shadow: 0 15px 30px rgba(0,255,255,0.7);
    }
    .flash-message {
      padding: 10px;
      border-radius: 8px;
      margin-bottom: 10px;
      text-align: center;
      background: #1abc9c;
      color: black;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>📩 Instagram Inbox Sender</h1>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        {% for message in messages %}
          <div class="flash-message">{{ message }}</div>
        {% endfor %}
      {% endif %}
    {% endwith %}
    <form method="POST" enctype="multipart/form-data">
      <label>Instagram Username:</label>
      <input type="text" name="username" required />

      <label>Password:</label>
      <input type="password" name="password" required />

      <label>Target Usernames (comma-separated):</label>
      <input type="text" name="target_ids" placeholder="e.g. user1, user2" required />

      <label>Message File (.txt):</label>
      <input type="file" name="message_file" accept=".txt" required />

      <label>Delay (seconds):</label>
      <input type="number" name="delay" value="5" min="0" required />

      <button type="submit">🚀 Start Sending</button>
    </form>
    <form method="POST" action="/stop">
      <button type="submit">✋ Stop Sending</button>
    </form>
  </div>
</body>
</html>
'''

# Sending logic with challenge + session handling
def send_messages(username, password, target_ids, messages, delay):
    global stop_flag
    stop_flag = False
    try:
        cl = Client()
        cl.delay_range = [1, 3]

        # Load session if exists
        if os.path.exists("session.json"):
            cl.load_settings("session.json")

        try:
            cl.login(username, password)
            cl.dump_settings("session.json")
        except Exception as e:
            print("[LOGIN WARNING]", e)
            if "challenge" in str(e).lower():
                try:
                    cl.challenge_resolve_auto()
                    cl.login(username, password)
                    cl.dump_settings("session.json")
                except Exception as ce:
                    print("[ERROR] Challenge Failed:", ce)
                    return
            else:
                print("[LOGIN FAILED]:", e)
                return

        targets = [x.strip() for x in target_ids.split(",") if x.strip()]
        for target in targets:
            user_id = cl.user_id_from_username(target)
            for message in messages:
                if stop_flag:
                    print("[STOPPED] Sending interrupted.")
                    return
                cl.direct_send(message, user_ids=[user_id])
                print(f"[SENT] To {target}: {message}")
                time.sleep(delay)
        print("[DONE] All messages sent.")
    except Exception as e:
        print("[ERROR]", e)

@app.route("/", methods=["GET", "POST"])
def index():
    global stop_flag
    if request.method == "POST":
        stop_flag = False
        try:
            username = request.form["username"]
            password = request.form["password"]
            target_ids = request.form["target_ids"]
            delay = int(request.form["delay"])
            file = request.files["message_file"]
            messages = file.read().decode("utf-8").splitlines()
            messages = [m.strip() for m in messages if m.strip()]
            if not messages:
                flash("Message file is empty!")
                return redirect(url_for("index"))

            threading.Thread(target=send_messages, args=(username, password, target_ids, messages, delay)).start()
            flash("✅ Messages are being sent in the background.")
        except Exception as e:
            flash(f"❌ Error: {e}")
    return render_template_string(HTML_TEMPLATE)

@app.route("/stop", methods=["POST"])
def stop():
    global stop_flag
    stop_flag = True
    flash("⛔ Sending stopped.")
    return redirect(url_for("index"))

# Run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
  
