import os
import secrets
import smtplib
import sqlite3
from email.mime.text import MIMEText

from flask import Flask, render_template, request, redirect, session, flash, send_from_directory

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
if not app.secret_key:
    raise RuntimeError("Set FLASK_SECRET_KEY before starting the application.")


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


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        conn = sqlite3.connect("portfolio.db")
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO messages (name,email,message) VALUES (?,?,?)",
            (name, email, message),
        )
        conn.commit()
        conn.close()

        sender_email = os.environ.get("EMAIL_ADDRESS")
        app_password = os.environ.get("EMAIL_PASSWORD")
        if not sender_email or not app_password:
            flash("Your message was saved, but email notifications are not configured.")
            return redirect("/contact")

        body = f"""Name: {name}
Email: {email}

Message:
{message}
"""
        msg = MIMEText(body)
        msg["Subject"] = "New Contact Form Message"
        msg["From"] = sender_email
        msg["To"] = sender_email

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, app_password)
                server.send_message(msg)
        except (OSError, smtplib.SMTPException):
            flash("Your message was saved, but the email notification could not be sent.")
            return redirect("/contact")

        flash("Your message has been sent successfully!")
        return redirect("/contact")

    return render_template("contact.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        expected_username = os.environ.get("ADMIN_USERNAME")
        expected_password = os.environ.get("ADMIN_PASSWORD")

        if (
            expected_username
            and expected_password
            and secrets.compare_digest(username, expected_username)
            and secrets.compare_digest(password, expected_password)
        ):
            session["admin"] = True
            return redirect("/dashboard")
        return "Invalid Credentials", 401

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


@app.route("/resume")
def resume():
    return send_from_directory("static", "resume.pdf")


@app.route("/projects")
def project():
    return render_template("project.html")


if __name__ == "__main__":
    init_db()
    app.run(debug=False)
