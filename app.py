from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secretkey"


def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# HOME PAGE
@app.route("/")
def home():
    db = get_db()
    items = db.execute("SELECT * FROM items").fetchall()
    return render_template("index.html", items=items)


# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()

        db.execute(
            "INSERT INTO users(name,email,password) VALUES (?,?,?)",
            (name, email, password)
        )

        db.commit()

        return redirect("/login")

    return render_template("register.html")


# LOGIN
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        db = get_db()

        user = db.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        ).fetchone()

        if user and user["password"] == password:

            session["user_id"] = user["id"]

            return redirect("/")

        else:
            return "Invalid Email or Password"

    return render_template("login.html")


# REPORT ITEM
@app.route("/report", methods=["GET", "POST"])
def report():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        location = request.form["location"]
        type_item = request.form["type"]

        db = get_db()

        db.execute(
            "INSERT INTO items(title,description,location,type,user_id) VALUES (?,?,?,?,?)",
            (title, description, location, type_item, session["user_id"])
        )

        db.commit()

        return redirect("/")

    return render_template("report.html")


@app.route("/claim/<int:item_id>", methods=["GET","POST"])
def claim(item_id):

    if "user_id" not in session:
        return redirect("/login")

    db = get_db()

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]
        message = request.form["message"]

        db.execute("""
        INSERT INTO claims(item_id,user_id,name,phone,email,message)
        VALUES (?,?,?,?,?,?)
        """,(item_id, session["user_id"], name, phone, email, message))

        db.commit()

        return redirect("/")

    return render_template("claim.html", item_id=item_id)

# SEARCH
@app.route("/search")
def search():

    query = request.args.get("q")

    db = get_db()

    items = db.execute(
        "SELECT * FROM items WHERE title LIKE ?",
        ("%"+query+"%",)
    ).fetchall()

    return render_template("index.html", items=items)


if __name__ == "__main__":
    app.run(debug=True)
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    db = get_db()

    claims = db.execute("""
    SELECT items.title, claims.name, claims.phone, claims.email, claims.message
    FROM claims
    JOIN items ON claims.item_id = items.id
    WHERE items.user_id = ?
    """, (session["user_id"],)).fetchall()

    return render_template("dashboard.html", claims=claims)




