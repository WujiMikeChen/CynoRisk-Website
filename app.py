from flask import Flask, render_template, request

app = Flask(
    __name__,
    static_folder='assets',            # instead of /static
    template_folder='.'                # use root dir or any folder
)


@app.route("/")
def home():
    return render_template('index.html')