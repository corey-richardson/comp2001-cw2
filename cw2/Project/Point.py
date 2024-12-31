from flask import abort, make_response, request

from Authentication import require_auth
from config import db
from models import Point, PointSchema

@require_auth
def create():
    """PROTECTED ENDPOINT: Create a new Point in the database."""
    point = request.get_json()
    
    next_point_id = point.get("next_point_id")
    previous_point_id = point.get("previous_point_id")
    
    # Check required fields exists
    required_fields = ["latitude", "longitude"]
    missing_fields = [field for field in required_fields if not point.get(field)]
    if missing_fields:
        abort(400, f"Missing required fields: {', '.join(missing_fields)}")
    
    # Validate next_point_id and previous_point_id exist if provided
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


def read_one(point_id):
    """Fetch a single Point from the database, queried by it's ID, else return 404."""
    point = Point.query.get_or_404(point_id)
    return PointSchema().dump(point), 200
    

def read_all():
    """Fetch all points in the database."""
    points = Point.query.all()
    return PointSchema(many = True).dump(points), 200


@require_auth
def update(point_id):
    """PROTECTED ENDPOINT: Update a Point in the database, indicated by it's ID."""
    point = request.get_json()
    existing_point = Point.query.get_or_404(point_id)
    
    for key, value in point.items():
        if hasattr(existing_point, key):
            setattr(existing_point, key, value)
    
    db.session.commit()
    return PointSchema().dump(existing_point), 200
    

@require_auth
def delete(point_id):
    """PROTECTED ENDPOINT: Delete a Point from the database, indicated by it's ID."""
    existing_point = Point.query.get_or_404(id)
    db.session.delete(existing_point)
    db.session.commit()
    return make_response(f"Point with ID {point_id} deleted.", 204)
