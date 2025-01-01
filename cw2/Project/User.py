from flask import abort, make_response, request

from Authentication import require_auth
from config import db
from models import User, UserSchema

@require_auth
def create():
    """PROTECTED ENDPOINT: Create a new User in the database."""
    user = request.get_json()
    
    # Check required field exists
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


@require_auth
def read_one(user_id):
    """Fetch a single User from the database, queried by it's ID, else return 404."""
    user = User.query.get_or_404(user_id)
    return UserSchema().dump(user), 200


@require_auth
def read_all():
    """Fetch all users in the database."""
    users = User.query.all()
    return UserSchema(many = True).dump(users), 200


@require_auth
def update(user_id):
    """PROTECTED ENDPOINT: Update a User in the database, indicated by it's ID."""
    user = request.get_json()
    existing_user = User.query.get_or_404(user_id)
    
    for key, value in user.items():
        if hasattr(existing_user, key):
            setattr(existing_user, key, value)
        
    db.session.commit()
    return UserSchema().dump(existing_user), 200


@require_auth
def delete(user_id):
    """PROTECTED ENDPOINT: Delete a User from the database, indicated by it's ID."""
    existing_user = User.query.get_or_404(user_id)
    db.session.delete(existing_user)
    db.session.commit()
    return make_response(f"User with ID {user_id} deleted.", 204)
