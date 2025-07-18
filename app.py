from flask import Flask, request, render_template_string, redirect, url_for
import os, threading, time
from instagrapi import Client

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

stop_flag = {"stop": False}

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Instagram Message Sender</title>
    <style>
        body {
            margin: 0;
            background: #000;
            font-family: 'Segoe UI', sans-serif;
            color: white;
        }
        .wrapper {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(to bottom, #000000, #050505);
        }
        .box {
            background: rgba(0,0,0,0.8);
            border-radius: 20px;
            padding: 40px 30px;
            box-shadow: 0 0 25px rgba(0,255,255,0.2);
            width: 100%%;
            max-width: 400px;
            backdrop-filter: blur(10px);
        }
        h2 {
            text-align: center;
            margin-bottom: 30px;
            background: linear-gradient(to right, #00ffff, #00bfff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 24px;
        }
        label {
            font-weight: bold;
            margin-top: 10px;
            display: block;
        }
        input[type="text"], input[type="password"], input[type="number"], input[type="file"] {
            width: 100%%;
            padding: 10px;
            margin: 8px 0;
            border: none;
            border-radius: 10px;
            background: rgba(255,255,255,0.1);
            color: white;
        }
        .btn {
            width: 100%%;
            padding: 12px;
            margin-top: 15px;
            background: linear-gradient(45deg, #00e1ff, #00bfff);
            border: none;
            border-radius: 12px;
            font-weight: bold;
            color: white;
            cursor: pointer;
            box-shadow: 0 5px 15px rgba(0,255,255,0.4);
            transition: all 0.3s ease;
        }
        .btn:hover {
            transform: scale(1.03);
            box-shadow: 0 10px 30px rgba(0,255,255,0.6);
        }
    </style>
</head>
<body>
    <div class="wrapper">
        <div class="box">
            <h2>📩 Instagram Message Sender</h2>
            <form method="POST" enctype="multipart/form-data">
                <label>Username:</label>
                <input type="text" name="username" required>

                <label>Password:</label>
                <input type="password" name="password" required>

                <label>Target Username or Chat ID:</label>
                <input type="text" name="target" required>

                <label>Delay (in seconds):</label>
                <input type="number" name="delay" value="5" min="0">

                <label>Message File (messages.txt):</label>
                <input type="file" name="message_file" required>

                <button type="submit" class="btn">🚀 Start Sending</button>
            </form>
            <form method="POST" action="/stop">
                <button type="submit" class="btn">✋ Stop Sending</button>
            </form>
        </div>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        stop_flag["stop"] = False
        username = request.form["username"]
        password = request.form["password"]
        target = request.form["target"]
        delay = int(request.form.get("delay", 5))

        message_path = os.path.join(UPLOAD_FOLDER, "messages.txt")
        request.files["message_file"].save(message_path)

        with open(message_path, "r") as f:
            messages = [line.strip() for line in f if line.strip()]

        def send_messages():
            try:
                cl = Client()
                cl.login(username, password)
                if target.isdigit():
                    thread_id = target
                else:
                    user_id = cl.user_id_from_username(target)
                    thread_id = cl.direct_create(user_ids=[user_id]).id

                for msg in messages:
                    if stop_flag["stop"]:
                        print("⛔ Sending stopped.")
                        break
                    cl.direct_send(text=msg, thread_ids=[thread_id])
                    print(f"✅ Sent: {msg}")
                    time.sleep(delay)
                print("🎉 Done.")
            except Exception as e:
                print("❌ Error:", e)

        threading.Thread(target=send_messages).start()
        return "<h3 style='color:lime;'>✅ Sending started! Keep tab open. Use STOP to cancel.</h3>"

    return render_template_string(HTML)

@app.route("/stop", methods=["POST"])
def stop():
    stop_flag["stop"] = True
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
    
