from flask import Flask, request, render_template_string
import os, time
import instagrapi
from instagrapi import Client

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Instagram Message Sender</title>
    <style>
        body {
            margin: 0;
            font-family: 'Segoe UI', sans-serif;
            background: url('https://wallpaperaccess.com/full/1567664.jpg') no-repeat center center fixed;
            background-size: cover;
            color: white;
        }
        .container {
            width: 90%%;
            max-width: 700px;
            margin: 60px auto;
            background: rgba(0, 0, 0, 0.7);
            border-radius: 20px;
            box-shadow: 0 0 30px skyblue;
            padding: 30px;
            backdrop-filter: blur(10px);
        }
        h2 {
            text-align: center;
            color: #00e1ff;
            text-shadow: 2px 2px 10px #00bfff;
        }
        label, input, textarea {
            display: block;
            width: 100%%;
            margin-bottom: 10px;
        }
        input, textarea {
            padding: 10px;
            border: none;
            border-radius: 10px;
            background: rgba(255,255,255,0.1);
            color: white;
        }
        input[type=submit] {
            background: linear-gradient(45deg, #00e1ff, #00bfff);
            box-shadow: 0 5px 15px rgba(0,255,255,0.4);
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        input[type=submit]:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 25px rgba(0,255,255,0.6);
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>📨 Instagram Message Sender</h2>
        <form method="POST" enctype="multipart/form-data">
            <label>📛 Username:</label>
            <input type="text" name="username" required>

            <label>🔐 Password:</label>
            <input type="password" name="password" required>

            <label>🎯 Target Username or Chat ID:</label>
            <input type="text" name="target" required>

            <label>⏳ Delay (in seconds):</label>
            <input type="number" name="delay" value="5" min="0">

            <label>📄 Message File (messages.txt):</label>
            <input type="file" name="message_file" required>

            <label>🚫 Haters File (usernames to skip - optional):</label>
            <input type="file" name="haters_file">

            <input type="submit" value="🚀 Send Messages">
        </form>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        target = request.form["target"]
        delay = int(request.form.get("delay", 5))

        message_path = os.path.join(UPLOAD_FOLDER, "messages.txt")
        haters_path = os.path.join(UPLOAD_FOLDER, "haters.txt")

        request.files["message_file"].save(message_path)
        if "haters_file" in request.files and request.files["haters_file"].filename:
            request.files["haters_file"].save(haters_path)
            with open(haters_path, "r") as f:
                haters = [line.strip().lower() for line in f if line.strip()]
        else:
            haters = []

        with open(message_path, "r") as f:
            messages = [line.strip() for line in f if line.strip()]

        cl = Client()
        try:
            cl.login(username, password)
        except Exception as e:
            return f"<h3>Login Failed: {str(e)}</h3>"

        try:
            if target.isdigit():
                thread_id = target
            else:
                user_id = cl.user_id_from_username(target)
                thread_id = cl.direct_create(user_ids=[user_id]).id

            for msg in messages:
                if target.lower() in haters:
                    continue
                cl.direct_send(text=msg, thread_ids=[thread_id])
                time.sleep(delay)

            return "<h2>✅ Messages sent successfully!</h2>"
        except Exception as e:
            return f"<h3>Failed to send messages: {str(e)}</h3>"

    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
    
