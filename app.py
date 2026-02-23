import os
import smtplib
from email.mime.text import MIMEText
import sqlite3
from flask import Flask, render_template, request, redirect, session, flash

app = Flask(__name__)
app.secret_key = "supersecret"

def init_db():
    conn = sqlite3.connect("portfolio.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        # Save to database
        conn = sqlite3.connect("portfolio.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO messages (name,email,message) VALUES (?,?,?)",
                    (name, email, message))
        conn.commit()
        conn.close()

        # Send Email
        sender_email = "niranjanyadav8044@gmail.com"
        app_password = os.environ.get("EMAIL_PASSWORD")

        if not app_password:
            raise ValueError("EMAIL_PASSWORD environment variable not set!")

        subject = "New Contact Form Message"
        body = f"""
        Name: {name}
        Email: {email}

        Message:
        {message}
        """

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = sender_email

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
        flash("Your message has been sent successfully!")

    return render_template("contact.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":
            session["admin"] = True
            return redirect("/dashboard")
        else:
            return "Invalid Credentials"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "admin" not in session:
        return redirect("/login")

    conn = sqlite3.connect("portfolio.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages")
    messages = cur.fetchall()
    conn.close()

    return render_template("dashboard.html", messages=messages)

from flask import send_from_directory

@app.route("/resume")
def resume():
    return send_from_directory("static", "resume.pdf")

@app.route("/projects")
def project():
    return render_template("project.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
