from authentication import authenticate
from config import db
from models import User, UserSchema, Trail, TrailSchema, Point, PointSchema

from flask import abort, make_response

def create(user):
    required_fields = ["email", "role"]
    missing_fields = [field for field in required_fields if not user.get(field)]
    if missing_fields:
        abort(400, f"Missing required fields: {', '.join(missing_fields)}")
        
    try:
        new_user = UserSchema().load(user, session = db.session)
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, f"Error creating new user: {str(e)}")
    
    return UserSchema().dump(new_user), 201


def read_one(id):
    user = User.query.get_or_404(id)
    return UserSchema().dump(user), 200

    
def read_all():
    users = User.query.all()
    return UserSchema(many = True).dump(users), 200


def update(id, user):
    existing_user = User.query.get_or_404(id)
    for key, value in user.items():
        setattr(existing_user, key, value)
    db.session.commit()
    return UserSchema().dump(existing_user), 201

    
def delete(id):
    existing_user = User.query.get_or_404(id)
    db.session.delete(existing_user)
    db.session.commit()
    return make_response(f"User with ID {id} deleted.", 204)
