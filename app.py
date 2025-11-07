# app.py
import os
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from dotenv import load_dotenv

# load local .env for development (won't be used on Render)
load_dotenv()

app = Flask(__name__)

# Use environment variables (set them locally in .env and on Render in settings)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() in ('true', '1', 'yes')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        try:
            msg = Message(
                subject=f"Portfolio Contact from {name or 'Anonymous'}",
                sender=app.config['MAIL_USERNAME'],
                recipients=[app.config['MAIL_USERNAME']],
                body=f"From: {name}\nEmail: {email}\n\nMessage:\n{message}"
            )
            mail.send(msg)
            flash("Your message has been sent successfully!", "success")
        except Exception as e:
            # log error to stderr so Render / Heroku logs show it
            import sys
            print("Error sending email:", e, file=sys.stderr)
            flash("Error sending email. Check server logs or your mail settings.", "danger")

        return redirect(url_for('home'))

    return render_template('index.html')

if __name__ == '__main__':
    # Local run: pick port from env for parity with Render
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
