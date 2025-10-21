from flask import Flask, render_template
from app.routes.stego import stego_bp
from app.routes.decrypt_stego import decrypt_bp
from app.routes.masko import stegomask_bp

app = Flask(
    __name__,
    template_folder="app/templates",
    static_folder="app/static"
)

app.secret_key = "supersecretkey"
app.register_blueprint(stego_bp)
app.register_blueprint(decrypt_bp)
app.register_blueprint(stegomask_bp)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")


# Only run Flask dev server when executing this file directly
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
