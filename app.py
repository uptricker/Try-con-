_':
    app.run(host='0.0.0.0', port=5000)
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>H4CK3R | ZONE</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      margin: 0;
      padding: 0;
      font-family: 'Courier New', monospace;
      background: radial-gradient(circle at top left, #000000 0%, #0d0d0d 100%);
      background-image: url('https://i.ibb.co/8Bq1Bgy/cyber-bg.jpg');
      background-size: cover;
      background-position: center;
      color: #00ffcc;
    }

    .wrapper {
      backdrop-filter: blur(10px);
      background-color: rgba(0, 0, 0, 0.6);
      max-width: 900px;
      margin: 30px auto;
      padding: 40px 20px;
      border-radius: 15px;
      box-shadow: 0 0 25px #00ffee;
    }

    h1 {
      font-size: 3em;
      text-align: center;
      margin-bottom: 30px;
      text-shadow: 0 0 20px #00f2ff;
      animation: glow 2s ease-in-out infinite alternate;
    }

    @keyframes glow {
      from {
        text-shadow: 0 0 10px #00ffee;
      }
      to {
        text-shadow: 0 0 30px #00ffee, 0 0 60px #00ffee;
      }
    }

    .btn {
      display: inline-block;
      margin: 12px;
      padding: 15px 30px;
      font-size: 1.1em;
      color: #fff;
      text-decoration: none;
      border-radius: 50px;
      border: 2px solid #00ffee;
      background: transparent;
      transition: all 0.3s ease;
      box-shadow: 0 0 15px #00ffee;
    }

    .btn:hover {
      background-color: #00ffee;
      color: #000;
      box-shadow: 0 0 25px #00ffee, 0 0 50px #00ffee;
      transform: scale(1.05);
    }

    .section {
      margin-top: 40px;
      background-color: rgba(0, 0, 0, 0.4);
      padding: 20px;
      border-radius: 12px;
      box-shadow: 0px 0px 20px #00ffe0;
    }

    .section h2 {
      color: #00f2ff;
    }

    @media screen and (max-width: 600px) {
      h1 { font-size: 2em; }
      .btn { font-size: 1em; padding: 10px 20px; }
    }
  </style>
</head>
<body>
  <div class="wrapper">
    <h1>👾 WELCOME TO HACKING ZONE</h1>

    <div class="button-group" style="text-align:center;">
      <a href="https://facebook.com/YOUR_FACEBOOK" class="btn" target="_blank">Facebook</a>
      <a href="https://instagram.com/YOUR_INSTAGRAM" class="btn" target="_blank">Instagram</a>
      <a href="https://wa.me/91YOURNUMBER" class="btn" target="_blank">WhatsApp</a>
    </div>

    <div class="section">
      <h2>🧠 About Me</h2>
      <p>I’m a cyber security enthusiast & ethical hacker. This site shares educational info & awareness tools.</p>
    </div>

    <div class="section">
      <h2>⚠️ Disclaimer</h2>
      <p>This site is strictly for educational use only. We do not support or encourage any illegal hacking activities.</p>
    </div>

    <div class="section">
      <h2>📬 Contact</h2>
      <p><b>WhatsApp:</b> +91XXXXXXXXXX</p>
      <p><b>Email:</b> your@email.com</p>
      <p><b>Telegram:</b> https://t.me/YOUR_TELEGRAM</p>
    </div>
  </div>
</body>
</html>
""")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
