from flask import render_template, request, jsonify

from models import User, Trail, Point, TrailFeature, Feature

import config
from config import db, ma

app = config.connex_app
flask_app = app.app
app.add_api(config.basedir / "swagger.yml")

@app.route("/")
def home():
    return render_template("index.html")

# @app.route('/api/user', methods=['GET'])
# def get_users():
#     users = User.query.all()
#     return jsonify([{'email': user.email, 'role': user.role} for user in users])

# @app.route('/api/users/<int:id>', methods=['GET'])
# def get_user(id):
#     user = User.query.get(id)
#     if user is None:
#         return jsonify({'message': 'User not found'}), 404
#     return jsonify({'email': user.email, 'role': user.role})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
    