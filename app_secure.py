# secure version with password hashing

from flask import Flask, render_template, request, redirect, session
import sqlite3
import bcrypt
import time
import os
import secrets
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=False,
    SESSION_COOKIE_SAMESITE="Lax"
)
attempts = {}
def connect_db():
    return sqlite3.connect("database.db")
@app.route("/")
def home():
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if len(password) < 6:
            return "Password must be at least 6 characters"
        db = connect_db()
        existing = db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        if existing:
            return "User already exists"
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())         # hashed password for security
        db.execute(
            "INSERT INTO users (email, password, role) VALUES (?, ?, ?)",
            (email, hashed, "USER")
        )
        db.commit()
        return redirect("/login")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if email in attempts:
            if attempts[email]["count"] >= 5:               #brute force attack prevention
                if time.time() - attempts[email]["time"] < 30:
                    return "Too many attempts. Try later."
        db = connect_db()
        user = db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        if not user:
            return "Invalid credentials"
        stored = user[2]
        if not bcrypt.checkpw(password.encode(), stored):    #password verification auth sucurity
            if email not in attempts:
                attempts[email] = {"count": 1, "time": time.time()}
            else:
                attempts[email]["count"] += 1
            db.execute(
                "INSERT INTO audit_logs (email, action) VALUES (?, ?)",
                (email, "failed login")
            )
            db.commit()
            return "Invalid credentials"      #NO USER ENUMERATION
        attempts[email] = {"count": 0, "time": 0}
        session["user"] = email
        db.execute(
            "INSERT INTO audit_logs (email, action) VALUES (?, ?)",
            (email, "login success")
        )
        db.commit()
        return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    db = connect_db()
    q = request.args.get("q", "")
    if q:
        notes = db.execute(
            "SELECT * FROM notes WHERE owner_email=? AND (title LIKE ? OR content LIKE ?)",#only show user's own notes, prevents data leakage
            (session["user"], f"%{q}%", f"%{q}%")
        ).fetchall()
    else:
        notes = db.execute(
            "SELECT * FROM notes WHERE owner_email=?",     #only show user's own notes, prevents data leakage
            (session["user"],)
        ).fetchall()
    return render_template("dashboard.html", notes=notes, search=q)

@app.route("/add_note", methods=["POST"])
def add_note():
    if "user" not in session:
        return redirect("/login")
    title = request.form["title"]
    content = request.form["content"]
    db = connect_db()
    db.execute(
        "INSERT INTO notes (title, content, owner_email) VALUES (?, ?, ?)",
        (title, content, session["user"])
    )
    db.commit()
    return redirect("/dashboard")
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        email = request.form["email"]
        token = secrets.token_hex(16) # Generate a secure random token
        db = connect_db()
        db.execute(
            "INSERT INTO reset_tokens (email, token) VALUES (?, ?)",
            (email, token)
        )
        db.commit()
        return f"Reset link: /reset/{token}"
    return '''
        <h2>Forgot Password</h2>
        <form method="POST">
            <input name="email" placeholder="Email">
            <button>Send reset link</button>
        </form>
    '''

@app.route("/reset/<token>", methods=["GET", "POST"])
def reset(token):
    db = connect_db()
    row = db.execute(
        "SELECT email FROM reset_tokens WHERE token=?",
        (token,)
    ).fetchone()
    if not row:
        return "Invalid token"
    if request.method == "POST":
        new_password = request.form["password"]
        if len(new_password) < 6:
            return "Password too short"
        hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        db.execute(
            "UPDATE users SET password=? WHERE email=?",
            (hashed, row[0])
        )
        db.execute(
            "DELETE FROM reset_tokens WHERE token=?", # Invalidate token after use
            (token,)
        )
        db.execute(
            "INSERT INTO audit_logs (email, action) VALUES (?, ?)", #log password reset action
            (row[0], "password reset")
        )
        db.commit()
        return "Password updated"
    return '''
        <h2>Reset Password</h2>
        <form method="POST">
            <input name="password" placeholder="New password">
            <button>Reset</button>
        </form>
    '''
app.run(debug=True)