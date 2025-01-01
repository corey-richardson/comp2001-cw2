from flask import abort, make_response, request

from Authentication import require_auth
from config import db
from models import TrailFeature, TrailFeatureSchema, Feature, FeatureSchema

@require_auth
def create():
    """PROTECTED ENDPOINT: Create a new Trail Feature link in the database."""
    trail_feature = request.get_json()
    
    trail_id = trail_feature.get("trail_id")
    feature_id = trail_feature.get("feature_id")
    
    # Check required field exists
    if not trail_id or not feature_id:
        abort(400, "Missing required fields.")
        
    try:
        new_link = TrailFeatureSchema().load(trail_feature, session = db.session)
        db.session.add(new_link)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, f"Error creating trail-feature link: {str(e)}")
        
    return TrailFeatureSchema().dump(trail_feature), 201


def read_one(trail_id, feature_id):
    """Fetch a single Trail Feature link from the database, queried by the 
    `trail_id` and `feature_id`, else return 404."""
    link = TrailFeature.query.get_or_404((trail_id, feature_id))
    return TrailFeatureSchema().dump(link), 200
    

def read_trail(trail_id):
    """Fetch all features linked to a Trail, indicated by the Trail's ID."""
    trail_features = TrailFeature.query.filter_by(trail_id=trail_id).all()
    if not trail_features:
        abort(404, "No features found for the given trail.")
    
    features = [Feature.query.get_or_404(tf.feature_id) for tf in trail_features]
    return FeatureSchema(many = True).dump(features), 200


def read_all():
    """Fetch all features in the database."""
    trail_features = TrailFeature.query.all()
    return TrailFeatureSchema(many = True).dump(trail_features), 200


@require_auth
def update(trail_id, feature_id):
    """PROTECTED ENDPOINT: Update a Trail Feature link in the database, 
    indicated by a `trail_id` and `feature_id` pair."""
    link = request.get_json()
    existing_link = TrailFeature.query.get_or_404((trail_id, feature_id))
    
    for key, value in link.items():
        if hasattr(existing_link, key):
            setattr(existing_link, key, value)
    
    db.session.commit()
    return TrailFeatureSchema().dump(existing_link), 200
    

@require_auth
def delete(trail_id, feature_id):
    """PROTECTED ENDPOINT: Delete a Trail Feature link from the database,
    indicated by a `trail_id` and `feature_id` pair."""
    existing_link = TrailFeature.query.get_or_404((trail_id, feature_id))
    db.session.delete(existing_link)
    db.session.commit()
    return make_response(f"Trail feature with ID {trail_id}:{feature_id} deleted.", 204)
