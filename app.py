from flask import Flask, request, render_template_string, flash, redirect, url_for
from instagrapi import Client
import os, time, threading

app = Flask(__name__)
app.secret_key = "your_secret_key"
stop_flag = False

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Instagram Inbox Sender</title>
    <style>
        body {
            margin: 0;
            background: url('https://wallpaperaccess.com/full/17450.jpg') no-repeat center center fixed;
            background-size: cover;
            font-family: 'Segoe UI', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: white;
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
        h2 {
            text-align: center;
            background: linear-gradient(to right, #00ffff, #00bfff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        label {
            margin-top: 10px;
            display: block;
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
        button {
            margin-top: 20px;
            width: 100%%;
            padding: 12px;
            background: linear-gradient(45deg, #00e1ff, #00bfff);
            border: none;
            border-radius: 10px;
            color: black;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 5px 15px rgba(0,255,255,0.4);
        }
        .flash-message {
            background: #1abc9c;
            padding: 10px;
            text-align: center;
            border-radius: 10px;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>📨 Instagram Inbox Sender</h2>
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            {% for message in messages %}
              <div class="flash-message">{{ message }}</div>
            {% endfor %}
          {% endif %}
        {% endwith %}
        <form method="POST" enctype="multipart/form-data">
            <label>Instagram Username:</label>
            <input type="text" name="username" placeholder="Your Instagram Username" required>

            <label>Password:</label>
            <input type="password" name="password" placeholder="Your Instagram Password" required>

            <label>Target Usernames (comma separated):</label>
            <input type="text" name="targets" placeholder="user1, user2" required>

            <label>Message File (.txt):</label>
            <input type="file" name="message_file" accept=".txt" required>

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

def send_messages(username, password, targets, messages, delay):
    global stop_flag
    stop_flag = False
    cl = Client()
    cl.delay_range = [1, 3]

    try:
        if os.path.exists("session.json"):
            cl.load_settings("session.json")
            print("[SESSION] Loaded")
        else:
            cl.login(username, password)
            cl.dump_settings("session.json")
            print("[LOGIN] New session created")

        for target in targets:
            user_id = cl.user_id_from_username(target)
            for msg in messages:
                if stop_flag:
                    print("[STOPPED]")
                    return
                cl.direct_send(msg, user_ids=[user_id])
                print(f"[SENT] {msg} to {target}")
                time.sleep(delay)
        print("[DONE] All messages sent.")

    except Exception as e:
        print("[ERROR]", e)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            username = request.form["username"]
            password = request.form["password"]
            targets = [x.strip() for x in request.form["targets"].split(",") if x.strip()]
            delay = int(request.form["delay"])
            file = request.files["message_file"]
            messages = [m.strip() for m in file.read().decode().splitlines() if m.strip()]
            threading.Thread(target=send_messages, args=(username, password, targets, messages, delay)).start()
            flash("✅ Message sending started.")
        except Exception as e:
            flash(f"❌ Error: {e}")
    return render_template_string(HTML)

@app.route("/stop", methods=["POST"])
def stop():
    global stop_flag
    stop_flag = True
    flash("⛔ Sending stopped.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
