from flask import render_template

import config
from config import db, ma

app = config.connex_app
flask_app = app.app
app.add_api(config.basedir / "swagger.yml")

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
    