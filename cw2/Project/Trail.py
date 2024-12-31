from Authentication import authenticate, require_auth
from config import db
from models import User, UserSchema, Trail, TrailSchema, Point, PointSchema, TrailFeature, TrailFeatureSchema, Feature, FeatureSchema

from flask import abort, make_response, request

# https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#client_error_responses

@require_auth
def create():
    trail = request.get_json()
    
    author_id = trail.get("author_id", None)
    starting_point_id = trail.get("starting_point_id", None)
    
    ## All required (non-nullable) fields are present
    required_fields = ["name", "summary", "description", "difficulty", "location", "length", "elevation_gain", "route_type"]
    missing_fields = [field for field in required_fields if not trail.get(field)]
    if missing_fields:
        abort(400, f"Missing required fields: {', '.join(missing_fields)}")

    # Fetch related objects and check they exists (FK constraint)
    if author_id:
        author = User.query.get(author_id)
        if not author:
            abort(404, f"User not found for Author ID: {author_id}")
    if starting_point_id:
        starting_point = Point.query.get(starting_point_id)
        if not starting_point:
            abort(404, f"Point not found for Point ID: {starting_point}")
        
    # Create new trail
    try:        
        new_trail = TrailSchema().load(trail, session = db.session)
                
        # author_id.trails.append(new_trail)
        db.session.add(new_trail)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, f"Error creating trail: {str(e)}")
    
    return TrailSchema().dump(new_trail), 201
        
        
def read_one(trail_id):
    trail = Trail.query.get_or_404(trail_id)
    return TrailSchema().dump(trail), 200
    

def read_all():
    trails = Trail.query.all()
    return TrailSchema(many = True).dump(trails), 200


@require_auth
def update(trail_id):
    trail = request.get_json()
    
    existing_trail = Trail.query.get_or_404(trail_id)
    for key, value in trail.items():
        setattr(existing_trail, key, value)
    db.session.commit()
    return TrailSchema().dump(existing_trail), 201
    

@require_auth
def delete(trail_id):
    existing_trail = Trail.query.get_or_404(trail_id)
    db.session.delete(existing_trail)
    db.session.commit()
    return make_response(f"Trail with ID {id} deleted.", 204)
