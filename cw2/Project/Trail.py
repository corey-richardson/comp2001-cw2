from authentication import authenticate
from config import db
from models import User, UserSchema, Trail, TrailSchema, Point, PointSchema

from flask import abort, make_response

def create(trail):
    author_id = trail.get("author_id")
    starting_point_id = trail.get("id")
    name = trail.get("id")
    summary = trail.get("id")
    description = trail.get("id")
    location = trail.get("id")
    length = trail.get("id")
    elevation_gain = trail.get("id")
    route_type = trail.get("id")
    
    if not name:
        abort(400, "Trail Name is required.")
    if not summary:
        abort(400, "Trail Summary is required.")
    if not description:
        abort(400, "Trail Description is required.")
    if not location:
        abort(400, "Trail Location is required.")
    if not length:
        abort(400, "Trail Length is required.")
    if not elevation_gain:
        abort(400, "Trail Elevation Gain is required.")
    if not route_type:
        abort(400, "Trail Route Type is required.")
        
    author = User.query.get(author_id)
    starting_point = Point.query.get(starting_point_id)
    
    if author and starting_point:
        new_trail = TrailSchema.load(trail, session = db.session)
        author_id.trails.append(new_trail)
        db.session.commit()
        return TrailSchema.dump(new_trail), 201
    
    if not author:
        abort(404, f"User not found for Author ID: {author_id}")
    if not starting_point:
        abort(404, f"Point not found for Point ID: {starting_point}")
        
        
def read_one(id):
    trail = Trail.query.get(id)
    
    if trail is not None:
        return TrailSchema.dump(trail)
    
    abort(404, f"Trail with ID {id} not found.")