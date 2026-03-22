from flask import Flask, request, redirect, render_template, session, url_for
import pymysql
import bcrypt

app = Flask(__name__)
app.secret_key = "supersecretkey123"

# ---------------- DATABASE CONNECTION ----------------
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="system",
        database="chatapp",
        cursorclass=pymysql.cursors.DictCursor
    )

# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    # ✅ If already logged in → go to chat
    if "username" in session:
        return redirect(url_for("chat"))

    return render_template("homepage.html")

# ---------------- REGISTER PAGE ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = request.form["username"]
    password = request.form["password"]

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, hashed_password)
        )
        connection.commit()
    except pymysql.err.IntegrityError:
        return "Username already exists!"
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for("login"))

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login1CHAT.html")

    username = request.form["username"]
    password = request.form["password"]

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if user and bcrypt.checkpw(
        password.encode("utf-8"),
        user["password"].encode("utf-8")
    ):
        session["username"] = username
        return redirect(url_for("chat"))
    else:
        return render_template("login1CHAT.html", error="Invalid username or password")

# ---------------- CHAT PAGE ----------------
@app.route("/chat")
def chat():
    if "username" not in session:
        return redirect("/login")

    print("LOGGED USER:", session["username"])  # 🔥 DEBUG

    return render_template("index.html", username=session["username"])
# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ---------------- RUN ----------------
if __name__ == "__main__":
    print("RUNNING DATABASE.PY ✅")
    app.run(debug=True)