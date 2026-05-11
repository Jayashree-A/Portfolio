from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secretkey123"

# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect("messages.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        message TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------- HOME ----------
@app.route("/")
def home():
    return render_template("index.html")

# ---------- CONTACT ----------
@app.route("/contact", methods=["POST"])
def contact():
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    conn = sqlite3.connect("messages.db")
    cur = conn.cursor()

    cur.execute("INSERT INTO contacts(name,email,message) VALUES(?,?,?)",
                (name, email, message))

    conn.commit()
    conn.close()

    return redirect(url_for("home"))

# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":
            session["user"] = username
            return redirect(url_for("admin"))

        return "Invalid login"

    return render_template("login.html")

# ---------- ADMIN ----------
@app.route("/admin")
def admin():
    if "user" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("messages.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM contacts")
    data = cur.fetchall()

    conn.close()

    return render_template("admin.html", data=data)

# ---------- DELETE MESSAGE ----------
@app.route("/delete/<int:id>")
def delete(id):
    if "user" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("messages.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM contacts WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("admin"))

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)