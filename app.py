from flask import Flask, request, render_template_string, redirect, url_for, flash
from instagrapi import Client
import os, time

app = Flask(__name__)
app.secret_key = "your_secret_key"

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Group Inbox</title>
    <style>
        body {
            margin: 0;
            font-family: 'Segoe UI', sans-serif;
            background: url('https://images.unsplash.com/photo-1621265736303-5381d1f5ec33?auto=format&fit=crop&w=1920&q=80') no-repeat center center fixed;
            background-size: cover;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: auto;
        }
        .container {
            background: rgba(0,0,0,0.85);
            padding: 40px 30px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,255,255,0.2);
            backdrop-filter: blur(10px);
            max-width: 500px;
            width: 90%%;
            color: white;
        }
        h1 {
            text-align: center;
            background: linear-gradient(to right, #00ffff, #00bfff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 26px;
            margin-bottom: 25px;
        }
        label {
            font-weight: bold;
            display: block;
            margin-top: 15px;
        }
        input, select {
            width: 100%%;
            padding: 12px;
            margin-top: 6px;
            border: none;
            border-radius: 10px;
            background: rgba(255,255,255,0.1);
            color: white;
        }
        input::placeholder {
            color: #ccc;
        }
        .info {
            font-size: 12px;
            color: #aaa;
        }
        button {
            margin-top: 20px;
            width: 100%%;
            padding: 14px;
            font-size: 16px;
            font-weight: bold;
            background: linear-gradient(to right, #00ffff, #00bfff);
            border: none;
            border-radius: 12px;
            color: black;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 8px 20px rgba(0,255,255,0.5);
        }
        button:hover {
            transform: scale(1.05);
            box-shadow: 0 10px 30px rgba(0,255,255,0.7);
        }
        .flash-message {
            text-align: center;
            padding: 8px;
            margin-bottom: 15px;
            border-radius: 8px;
            background: #ff0040;
            color: white;
        }
        .success {
            background: #00c851;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📬 Instagram Group Inbox</h1>
        {% with messages = get_flashed_messages(with_categories=true) %}
          {% if messages %}
            {% for category, message in messages %}
              <div class="flash-message {{ category }}">{{ message }}</div>
            {% endfor %}
          {% endif %}
        {% endwith %}
        <form action="/" method="POST" enctype="multipart/form-data">
            <label>Instagram Username:</label>
            <input type="text" name="username" placeholder="Enter username" required>

            <label>Password:</label>
            <input type="password" name="password" placeholder="Enter password" required>

            <label>Send To:</label>
            <select name="choice" required>
                <option value="inbox">Inbox</option>
                <option value="group">Group</option>
            </select>

            <label>Target Username (Inbox):</label>
            <input type="text" name="target_username" placeholder="e.g. @someone">

            <label>Group Thread ID (Group):</label>
            <input type="text" name="thread_id" placeholder="e.g. 340282366841...">

            <label>Hater's Name:</label>
            <input type="text" name="haters_name" placeholder="Name of hater" required>

            <label>Message File:</label>
            <input type="file" name="message_file" required>
            <p class="info">One message per line</p>

            <label>Delay (seconds):</label>
            <input type="number" name="delay" value="5" min="0" required>

            <button type="submit">🚀 Send Messages</button>
        </form>
    </div>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def automate_instagram():
    if request.method == "POST":
        try:
            username = request.form["username"]
            password = request.form["password"]
            choice = request.form["choice"]
            target_username = request.form.get("target_username", "").strip()
            thread_id = request.form.get("thread_id", "").strip()
            delay = int(request.form["delay"])
            message_file = request.files["message_file"]

            messages = message_file.read().decode("utf-8").splitlines()
            messages = [m.strip() for m in messages if m.strip()]
            if not messages:
                flash("Message file is empty!", "error")
                return redirect(url_for("automate_instagram"))

            cl = Client()
            cl.login(username, password)
            flash("✅ Login successful!", "success")

            for message in messages:
                if choice == "inbox":
                    if not target_username:
                        flash("Target username required for inbox.", "error")
                        return redirect(url_for("automate_instagram"))
                    user_id = cl.user_id_from_username(target_username)
                    cl.direct_send(message, [user_id])
                    print(f"✅ Sent to {target_username}: {message}")
                elif choice == "group":
                    if not thread_id:
                        flash("Thread ID required for group message.", "error")
                        return redirect(url_for("automate_instagram"))
                    cl.direct_send(text=message, thread_ids=[thread_id])
                    print(f"✅ Sent to group {thread_id}: {message}")
                time.sleep(delay)

            flash("✅ All messages sent!", "success")
            return redirect(url_for("automate_instagram"))

        except Exception as e:
            flash(f"❌ Error: {str(e)}", "error")
            return redirect(url_for("automate_instagram"))

    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
