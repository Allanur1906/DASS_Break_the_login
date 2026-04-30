from flask import Flask, render_template, request, redirect, session
import sqlite3
import time

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    return sqlite3.connect("database.db")

@app.route("/")
def home():
    return redirect("/login")
#REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        db.execute(
            "INSERT INTO users (email, password, role, created_at) VALUES (?, ?, ?, ?)",
            (email, password, "USER", time.strftime("%Y-%m-%d %H:%M:%S"))
        )
        db.commit()
        db.close()
        return redirect("/login")
    return render_template("register.html")
# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        ).fetchone()

        if not user:
            db.close()
            return "User not found"
        else:
            if user[2] != password:
                db.close()
                return "Wrong password"
            else:
                session["user"] = email
                db.close()
                return redirect("/dashboard")

    return render_template("login.html")
# DASHBOARD
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    db = get_db()
    #SQL
    search = request.args.get("q", "")
    if search:
        notes = db.execute(
            "SELECT * FROM notes WHERE title LIKE '%" + search + "%' OR content LIKE '%" + search + "%'"
        ).fetchall()
    else:
        notes = db.execute("SELECT * FROM notes").fetchall()
    db.close()
    return render_template("dashboard.html", notes=notes, search=search)
# ADD_notE 
@app.route("/add_note", methods=["POST"])
def add_note():
    if "user" not in session:
        return redirect("/login")
    title = request.form["title"]
    content = request.form["content"]

    db = get_db()
    db.execute(
        "INSERT INTO notes (title, content, owner_email, created_at) VALUES (?, ?, ?, ?)",
        (title, content, session["user"], time.strftime("%Y-%m-%d %H:%M:%S"))
    )
    db.commit()
    db.close()
    return redirect("/dashboard")
# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
# PASSWORD RESET(predictable reusable token, no expiry)
@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        email = request.form["email"]
        token = email.replace("@", "_").replace(".", "_")

        db = get_db()
        db.execute(
            "INSERT INTO reset_tokens (email, token) VALUES (?, ?)",
            (email, token)
        )
        db.commit()
        db.close()

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
    db = get_db()
    row = db.execute(
        "SELECT email FROM reset_tokens WHERE token=?",
        (token,)
    ).fetchone()
    if not row:
        db.close()
        return "Invalid token"
    if request.method == "POST":
        new_password = request.form["password"]
        db.execute(
            "UPDATE users SET password=? WHERE email=?",
            (new_password, row[0])
        )
        db.commit()
        db.close()
        return "Password updated"
    db.close()
    return '''
        <h2>Reset Password</h2>
        <form method="POST">
            <input name="password" placeholder="New password">
            <button>Reset</button>
        </form>
    '''
if __name__ == "__main__":
    app.run(debug=True)
