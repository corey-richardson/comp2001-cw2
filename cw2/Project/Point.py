from authentication import authenticate
from config import db
from models import User, UserSchema, Trail, TrailSchema, Point, PointSchema, TrailFeature, TrailFeatureSchema, Feature, FeatureSchema
from flask import abort, make_response

def create(point):
    next_point_id = point.get("next_point_id")
    previous_point_id = point.get("previous_point_id")
    description = point.get("description")
    
    required_fields = ["latitude", "longitude"]
    missing_fields = [field for field in required_fields if not point.get(field)]
    if missing_fields:
        abort(400, f"Missing required fields: {', '.join(missing_fields)}")   
        
    if next_point_id is not None:
        next_point = Point.query.get(next_point_id)
        if not next_point:
            abort(404, f"Point not found for Point ID: {next_point_id}")
            
    if previous_point_id is not None:
        previous_point = Point.query.get(previous_point_id)
        if not previous_point:
            abort(404, f"Point not found for Point ID: {previous_point_id}")
            
    try:
        new_point = PointSchema().load(point, session = db.session)
        
        if next_point_id is not None:
            new_point.next_point = next_point
        if previous_point_id is not None:
            new_point.previous_point = previous_point
            
        db.session.add(new_point)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, f"Error creating point: {str(e)}")
        
    return PointSchema().dump(new_point), 201


def read_one(id):
    point = Point.query.get_or_404(id)
    return PointSchema().dump(point), 200
    

def read_all():
    points = Point.query.all()
    return PointSchema(many = True).dump(points), 200


def update(id, point):
    existing_point = Point.query.get_or_404(id)
    for key, value in point.items():
        setattr(existing_point, key, value)
    db.session.commit()
    return PointSchema().dump(existing_point), 201
    

def delete(id):
    existing_point = Point.query.get_or_404(id)
    db.session.delete(existing_point)
    db.session.commit()
    return make_response(f"Point with ID {id} deleted.", 204)
