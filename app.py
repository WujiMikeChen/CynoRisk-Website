from flask import Flask, request, render_template, redirect, flash
import os
from flask_mail import Mail, Message
from helper import is_valid_email_format,has_mx_record,allowed_file
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
users = {}

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT", 587))
app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS", "True") == "True"
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

mail = Mail(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact-us")
def contact_us_page():
    return render_template("contact-us.html")

@app.route("/about-us")
def about_us_page():
    return render_template("about-us.html")

@app.route("/risk-management")
def risk_management_page():
    return render_template("risk-management.html")

@app.route("/regulation")
def regulation_page():
    return render_template("regulation.html")

@app.route("/pricing")
def pricing_page():
    return render_template("pricing.html")

@app.route("/portfolio-management")
def portfolio_management_page():
    return render_template("portfolio-management.html")

@app.route("/journal")
def journal_page():
    return render_template("journal.html")

@app.route("/header.html")
def header_partial():
    return render_template("header.html")

@app.route("/contact-us.html")
def contact_partial():
    return render_template("contact-us.html")

@app.route("/articles/<article_name>")
def render_article(article_name):
    template_path = f"articles/{article_name}.html"
    full_path = os.path.join(app.template_folder, template_path)

    if os.path.exists(full_path):
        return render_template(template_path)
    else:
        return "Article not found", 404
    
@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")
    file = request.files.get('attachment')

    print(f"Received message from {name} ({email}): {message}")

    if not name or not email or not message:
        flash("All fields are required.")
        return redirect("/")
    
    if not is_valid_email_format(email):
        flash("Please enter a valid email address.")
        return redirect("/")

    if not has_mx_record(email):
        flash("That email domain can't receive mail.")
        return redirect("/")
    
    try:
        msg = Message(
            subject="New Contact Form Submission",
            sender=email,
            recipients=["wujimikechen@gmail.com"],
            body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        )
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            msg.attach(filename, file.content_type, file.read())
        mail.send(msg)
        flash("Message sent successfully!")
    except Exception as e:
        print("Email send failed:", e)
        flash("An error occurred while sending your message. Please try again.")

    return redirect("/")

# @app.route("/register", methods=["GET", "POST"])
# def register():
#     flash("Test flash")
#     if request.method == "POST":
#         username = request.form["username"]
#         email = request.form["email"]
#         password = request.form["password"]

#         if username in users:
#             flash("Username already exists.")
#             return redirect("/register")

#         users[username] = {
#             "email": email,
#             "password": generate_password_hash(password)
#         }
#         flash("Registration successful. You can now log in.")
#         return redirect("/login")

#     return render_template("register.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Validation
        if not username or not email or not password:
            flash("Please fill out all fields.")
            return redirect("/register")

        # Duplicate check
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("Username or email already exists.")
            return redirect("/register")

        # Save new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! You can now log in.")
        return redirect("/login")

    return render_template("register.html")


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]

#         user = users.get(username)
#         if user and check_password_hash(user["password"], password):
#             session["user"] = username
#             flash("Logged in successfully.")
#             return redirect("/")
#         else:
#             flash("Invalid username or password.")
#             return redirect("/login")

#     return render_template("login.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            flash("Login successful.")
            session['username'] = user.username  
            return redirect("/")
        else:
            flash("Invalid username or password.")
            return redirect("/login")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect("/")

# remove this later
if __name__ == "__main__":
    app.run(debug=True)