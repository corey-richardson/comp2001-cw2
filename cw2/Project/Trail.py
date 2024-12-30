from authentication import authenticate
from config import db
from models import User, UserSchema, Trail, TrailSchema, Point, PointSchema

from flask import abort, make_response

def create(trail):
    author_id = trail.get("author_id")
    starting_point_id = trail.get("id")
    
    required_fields = ["name", "summary", "description", "location", "length", "elevation_gain", "route_type"]
    missing_fields = [field for field in required_fields if not trail.get(field)]
    
    if missing_fields:
        abort(400, f"Missing required fields: {', '.join(missing_fields)}")

        
    author = User.query.get(author_id)
    starting_point = Point.query.get(starting_point_id)
    
    if not author:
        abort(404, f"User not found for Author ID: {author_id}")
    if not starting_point:
        abort(404, f"Point not found for Point ID: {starting_point}")

    try:        
        new_trail = TrailSchema.load(trail, session = db.session)
        author_id.trails.append(new_trail)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, f"Error creating trail: {str(e)}")
    
    return TrailSchema.dump(new_trail), 201
        
        
def read_one(id):
    trail = Trail.query.get(id)
    
    if trail is not None:
        return TrailSchema.dump(trail)
    
    abort(404, f"Trail with ID {id} not found.")