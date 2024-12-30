from config import db, ma

# https://marshmallow-sqlalchemy.readthedocs.io/en/latest/

from marshmallow_sqlalchemy import fields
from marshmallow import fields, validates
          
class Point(db.Model):
    __tablename__ = "CW2.Point"
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    next_point_id = db.Column(db.Integer, db.ForeignKey("CW2.Point.id"), nullable = True)
    previous_point_id = db.Column(db.Integer, db.ForeignKey("CW2.Point.id"), nullable = True)
    latitude = db.Column(db.Numeric(9, 6), nullable = False)
    longitude = db.Column(db.Numeric(9, 6), nullable = False)
    description = db.Column(db.String(127), nullable = True)
    
    # latitude = fields.Float(required=False)  # Make latitude optional
    # longitude = fields.Float(required=False)  # Make longitude optional
    
    next_point = db.relationship(
        "Point", remote_side=[id], foreign_keys=[next_point_id], backref="previous_points"
    )
    previous_point = db.relationship(
        "Point", remote_side=[id], foreign_keys=[previous_point_id], backref="next_points"
    )
    

class PointSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Point
        load_instance = True
        sqla_session = db.session
    
    next_point_id = fields.Integer()
    previous_point_id = fields.Integer()
        
    # https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html
    @validates("latitude")
    def validate_latitude(self, value):
        if not -90 <= value <= 90:
            raise ValueError(f"Failed Latitude Validation. Failed check: -90 <= {value} <= 90")
        
    @validates("longitude")
    def validate_longitude(self, value):
        if not -180 <= value <= 180:
            raise ValueError(f"Failed Longitude Validation. Failed check: -180 <= {value} <= 180")
       

class Trail(db.Model):
    __tablename__ = "CW2.Trail"
        
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    author_id = db.Column(db.Integer, db.ForeignKey("CW2.User.id"), nullable = True)
    starting_point_id = db.Column(db.Integer, db.ForeignKey("CW2.Point.id"), nullable = True)
    name = db.Column(db.String(255), nullable = False)
    summary = db.Column(db.String(255), nullable = False)
    description = db.Column(db.Text, nullable = False)
    difficulty = db.Column(db.String(9), nullable = False)
    location = db.Column(db.String(255), nullable = False)
    length = db.Column(db.Float, nullable = False)
    elevation_gain = db.Column(db.Integer, nullable = False)
    route_type = db.Column(db.String(15), nullable = False)
    
    # author = db.relationship("User", backref = "trails")
    starting_point = db.relationship("Point", foreign_keys = [starting_point_id])
    

class TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True
        sqla_session = db.session
    
    author_id = fields.Int(allow_none=True)
    starting_point_id = fields.Int(allow_none=True)
    
    # https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html
    @validates("route_type")
    def validate_route_type(self, value):
        valid_routes = ["Loop", "Out & back", "Point to point"]
        if value not in valid_routes:
            raise ValueError(f"Failed Route Type Validation: {value}. Must be in {valid_routes}")
        
          
class User(db.Model):
    __tablename__ = "CW2.User"
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String(255), nullable = False, unique = True)
    role = db.Column(db.String(6), nullable = False)
    
    trails = db.relationship(Trail, backref = "author")
    

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
      

class TrailFeature(db.Model):
    __tablename__ = "CW2.TrailFeature"
    
    trail_id = db.Column(db.Integer, db.ForeignKey("CW2.Trail.id"), primary_key = True, nullable = False)
    feature_id = db.Column(db.Integer, db.ForeignKey("CW2.Feature.id"), primary_key = True, nullable = False)

    trail = db.relationship("Trail", backref = db.backref("trail_features", lazy = True))
    

class TrailFeatureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrailFeature
        load_instance = True
        sqla_session = db.session

    trail_id = fields.Integer(required = True)
    feature_id = fields.Integer(required = True)
    
            
class Feature(db.Model):
    __tablename__ = "CW2.Feature"
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    feature = db.Column(db.String(255), nullable = False)
    
    trail_features = db.relationship("TrailFeature", backref = "feature", lazy = True)


class FeatureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Feature
        load_instance = True
        sqla_session = db.session
