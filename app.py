from flask import Flask, request, render_template, redirect, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact-us")
def contact_us_page():
    return render_template("contact-us.html")

@app.route("/about-us")
def about_us_page():
    return render_template("about-us.html")


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
    
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        
        print(f"Received message from {name} ({email}): {message}")
        flash("Message sent successfully!")
        return redirect("/contact-us")

    return render_template("contact-us.html")

# remove this later
if __name__ == "__main__":
    app.run(debug=True)

app.run()