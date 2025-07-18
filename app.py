from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>H4CK3R ZONE</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      margin: 0;
      padding: 0;
      font-family: 'Courier New', monospace;
      background: url('https://i.ibb.co/v1WwZqF/hack-bg.jpg') no-repeat center center fixed;
      background-size: cover;
      color: #00ffcc;
    }

    .container {
      text-align: center;
      padding: 40px 20px;
      background-color: rgba(0, 0, 0, 0.6);
      margin: 30px;
      border-radius: 15px;
      box-shadow: 0px 0px 20px #00ffee;
    }

    .title {
      font-size: 3em;
      margin-bottom: 30px;
      text-shadow: 0px 0px 10px #00f2ff;
    }

    .button-group .btn {
      display: inline-block;
      margin: 10px;
      padding: 15px 30px;
      font-size: 1.2em;
      border: none;
      border-radius: 12px;
      cursor: pointer;
      text-decoration: none;
      color: #fff;
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .btn.fb { background-color: #1877f2; }
    .btn.insta { background-color: #e1306c; }
    .btn.wa { background-color: #25d366; }

    .btn:hover {
      transform: scale(1.1);
      box-shadow: 0px 0px 20px #00ffee;
    }

    .section {
      margin-top: 40px;
      background-color: rgba(0, 0, 0, 0.5);
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0px 0px 20px #00ffe0;
    }

    @media only screen and (max-width: 600px) {
      .title { font-size: 2em; }
      .btn { font-size: 1em; padding: 10px 20px; }
    }
  </style>
</head>
<body>
  <div class="container">
    <h1 class="title">👨‍💻 HACKING ZONE</h1>

    <div class="button-group">
      <a href="https://facebook.com/YOUR_FACEBOOK" target="_blank" class="btn fb">Facebook</a>
      <a href="https://instagram.com/YOUR_INSTAGRAM" target="_blank" class="btn insta">Instagram</a>
      <a href="https://wa.me/91YOURNUMBER" target="_blank" class="btn wa">WhatsApp</a>
    </div>

    <div class="section about">
      <h2>About Me</h2>
      <p>I am an ethical hacker and cyber security enthusiast. This site is built for awareness and education.</p>
    </div>

    <div class="section disclaimer">
      <h2>Disclaimer</h2>
      <p>This website is intended only for educational and awareness purposes. We do not promote illegal activities.</p>
    </div>

    <div class="section contact">
      <h2>Contact Information</h2>
      <p><strong>WhatsApp:</strong> +91XXXXXXXXXX</p>
      <p><strong>Email:</strong> your@email.com</p>
      <p><strong>Telegram:</strong> https://t.me/YOUR_TELEGRAM</p>
    </div>
  </div>
</body>
</html>
""")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
