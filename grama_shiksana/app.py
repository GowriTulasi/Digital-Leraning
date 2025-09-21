from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "your_secret_key"   

# ---------------------- In-Memory User Storage ----------------------
users = {}

# ---------------------- INDEX / ROOT ----------------------
@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("home"))
    return redirect(url_for("login"))

# ---------------------- HOME ----------------------
@app.route("/home")
def home():
    if "username" not in session:
        flash("Please login first!", "warning")
        return redirect(url_for("login"))
    return render_template("home.html")

# ---------------------- SIGNUP ----------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Validation
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return render_template("signup.html")

        if username in users:
            flash("Username already exists!", "danger")
            return render_template("signup.html")

        # Save user
        users[username] = {
            "email": email,
            "password": password
        }

        flash("Account created successfully! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")

# ---------------------- LOGIN ----------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username]["password"] == password:
            session["username"] = username
            flash(f"Welcome, {username}!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password!", "danger")
            return render_template("login.html")
    return render_template("login.html")

# ---------------------- LOGOUT ----------------------
@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("You have been logged out.", "info")
    return render_template("logout.html")

# ---------------------- SUBJECT PAGES ----------------------
@app.route("/math")
def math_page():
    if "username" not in session:
        flash("Please login first!", "warning")
        return redirect(url_for("login"))
    return render_template("math.html")

@app.route("/science")
def science_page():
    if "username" not in session:
        flash("Please login first!", "warning")
        return redirect(url_for("login"))
    return render_template("science.html")

@app.route("/language")
def language_page():
    if "username" not in session:
        flash("Please login first!", "warning")
        return redirect(url_for("login"))
    return render_template("language.html")

@app.route("/ai_tutor")
def ai_tutor_page():
    if "username" not in session:
        flash("Please login first!", "warning")
        return redirect(url_for("login"))
    return render_template("ai_tutor.html")

@app.route("/recommendations")
def recommendations_page():
    if "username" not in session:
        flash("Please login first!", "warning")
        return redirect(url_for("login"))
    return render_template("recommendations.html")

# ---------------------- ABOUT ----------------------
@app.route("/about")
def about_page():
    return render_template("about.html")
# ---------------------- CONTACT ----------------------
@app.route("/contact", methods=["GET", "POST"])
def contact_page():
    if request.method == "POST":
        name = request.form["fullname"]
        email = request.form["email"]
        message = request.form["message"]
        flash("Your message has been received. We'll contact you soon.", "success")
        return redirect(url_for("contact_page"))
    return render_template("contact.html")

# ---------------------- 404 ERROR ----------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# ---------------------- RUN APP ----------------------
if __name__ == "__main__":
    app.run(debug=True)
