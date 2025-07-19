from flask import Flask, request, render_template_string, flash, redirect, url_for
from instagrapi import Client
import os, time, threading

app = Flask(__name__)
app.secret_key = "your_secret_key"
stop_flag = False

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Instagram Inbox Sender</title>
    <style>
        body {
            margin: 0;
            background: #000 url('https://wallpaperaccess.com/full/17450.jpg') no-repeat center center fixed;
            background-size: cover;
            font-family: 'Segoe UI', sans-serif;
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .box {
            background: rgba(0,0,0,0.8);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 0 30px cyan;
            width: 90%%;
            max-width: 500px;
        }
        h2 {
            text-align: center;
            font-size: 24px;
            background: linear-gradient(to right, #00ffff, #00bfff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        label {
            display: block;
            margin-top: 15px;
        }
        input {
            width: 100%%;
            padding: 10px;
            border: none;
            border-radius: 10px;
            background: rgba(255,255,255,0.1);
            color: white;
        }
        button {
            margin-top: 20px;
            width: 100%%;
            padding: 12px;
            font-weight: bold;
            border: none;
            border-radius: 12px;
            background: linear-gradient(to right, #00e1ff, #00bfff);
            color: black;
            box-shadow: 0 0 15px #00ffff;
            cursor: pointer;
        }
        .flash-message {
            background: #1abc9c;
            padding: 10px;
            text-align: center;
            margin-bottom: 15px;
            border-radius: 10px;
        }
    </style>
</head>
<body>
    <div class="box">
        <h2>📨 Instagram Inbox Sender</h2>
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            {% for message in messages %}
              <div class="flash-message">{{ message }}</div>
            {% endfor %}
          {% endif %}
        {% endwith %}
        <form method="POST" enctype="multipart/form-data">
            <label>Target Username(s) (comma separated):</label>
            <input type="text" name="targets" placeholder="user1, user2" required>

            <label>Message File (.txt):</label>
            <input type="file" name="message_file" required>

            <label>Delay (seconds):</label>
            <input type="number" name="delay" value="5" required>

            <button type="submit">🚀 Start Sending</button>
        </form>
        <form method="POST" action="/stop">
            <button type="submit">✋ Stop</button>
        </form>
    </div>
</body>
</html>
'''

def send_messages(targets, messages, delay):
    global stop_flag
    stop_flag = False
    try:
        cl = Client()
        cl.load_settings("session.json")  # No login, just load session

        for target in targets:
            user_id = cl.user_id_from_username(target)
            for msg in messages:
                if stop_flag:
                    print("[STOPPED]")
                    return
                cl.direct_send(msg, user_ids=[user_id])
                print(f"[SENT] {msg} to {target}")
                time.sleep(delay)

        print("[DONE] Messages sent.")
    except Exception as e:
        print("[ERROR]", e)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            targets = [t.strip() for t in request.form["targets"].split(",") if t.strip()]
            delay = int(request.form["delay"])
            file = request.files["message_file"]
            messages = [m.strip() for m in file.read().decode().splitlines() if m.strip()]
            threading.Thread(target=send_messages, args=(targets, messages, delay)).start()
            flash("✅ Message sending started.")
        except Exception as e:
            flash(f"❌ Error: {e}")
    return render_template_string(HTML_TEMPLATE)

@app.route("/stop", methods=["POST"])
def stop():
    global stop_flag
    stop_flag = True
    flash("⛔ Sending stopped.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
  
