from flask import abort, make_response, request

from Authentication import require_auth
from config import db
from models import Feature, FeatureSchema

@require_auth
def create():
    """PROTECTED ENDPOINT: Create a new Feature in the database."""
    feature = request.get_json()
    
    # Check required field exists
    # Uses same logic as other object types even though there is only 1 required field here
    # I thought it was best to have consistent logic in implementation.
    required_fields = ["feature"]
    missing_fields = [field for field in required_fields if not feature.get(field)]
    if missing_fields:
        abort(400, f"Missing required fields: {', '.join(missing_fields)}")  
        
    try:
        new_feature = FeatureSchema().load(feature, session = db.session)
        db.session.add(new_feature)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, f"Error creating feature: {str(e)}")
        
    return FeatureSchema().dump(feature), 201


def read_one(feature_id):
    """Fetch a single Feature from the database, queried by it's ID, else return 404."""
    feature = Feature.query.get_or_404(feature_id)
    return FeatureSchema().dump(feature), 200
    

def read_all():
    """Fetch all features in the database."""
    features = Feature.query.all()
    return FeatureSchema(many = True).dump(features), 200


@require_auth
def update(feature_id):
    """PROTECTED ENDPOINT: Update a Feature in the database, indicated by it's ID."""
    feature = request.get_json()
    existing_feature = Feature.query.get_or_404(feature_id)
    
    for key, value in feature.items():
        if hasattr(existing_feature, key):
            setattr(existing_feature, key, value)
    
    db.session.commit()
    return FeatureSchema().dump(existing_feature), 200
    

@require_auth
def delete(feature_id):
    """PROTECTED ENDPOINT: Delete a Feature from the database, indicated by it's ID."""
    existing_feature = Feature.query.get_or_404(feature_id)
    db.session.delete(existing_feature)
    db.session.commit()
    return make_response(f"Feature with ID {feature_id} deleted.", 204)
