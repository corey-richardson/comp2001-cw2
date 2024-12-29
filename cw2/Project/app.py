from flask import render_template

import config

app = config.connex_app
flask_app = app.app
# app.add_api(config.basedir / "swagger.yml")

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    print(flask_app.config["SQLALCHEMY_DATABASE_URI"])
    app.run(host="0.0.0.0", port=8000, debug=True)
    