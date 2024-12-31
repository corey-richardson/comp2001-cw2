from Authentication import authenticate, require_auth
from config import db
from models import User, UserSchema, Trail, TrailSchema, Point, PointSchema, TrailFeature, TrailFeatureSchema, Feature, FeatureSchema
from flask import abort, make_response, request

@require_auth
def create():
    feature = request.get_json()
    
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
        
    return FeatureSchema().dump(feature), 200


def read_one(feature_id):
    feature = Feature.query.get_or_404(feature_id)
    return FeatureSchema().dump(feature), 200
    

def read_all():
    features = Feature.query.all()
    return FeatureSchema(many = True).dump(features), 200


@require_auth
def update(feature_id):
    feature = request.get_json()
    existing_feature = Feature.query.get_or_404(feature_id)
    
    for key, value in feature.items():
        if hasattr(existing_feature, key):
            setattr(existing_feature, key, value)
    
    db.session.commit()
    return PointSchema().dump(existing_feature), 200
    

@require_auth
def delete(feature_id):
    existing_feature = Feature.query.get_or_404(id)
    db.session.delete(existing_feature)
    db.session.commit()
    return make_response(f"Feature with ID {feature_id} deleted.", 204)
