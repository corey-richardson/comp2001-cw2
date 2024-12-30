from config import db, ma

# https://marshmallow-sqlalchemy.readthedocs.io/en/latest/

from marshmallow_sqlalchemy import fields
from marshmallow import fields, validates
          
class Point(db.Model):
    __tablename__ = "Point"
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    next_point_id = db.Column(db.Integer, db.ForeignKey("Point.id"), nullable = True)
    previous_point_id = db.Column(db.Integer, db.ForeignKey("Point.id"), nullable = True)
    latitude = db.Column(db.Numeric(9, 6), nullable = False)
    longitude = db.Column(db.Numeric(9, 6), nullable = False)
    description = db.Column(db.String(127), nullable = True)
    
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
    __tablename__ = "Trail"
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    author_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable = True)
    starting_point_id = db.Column(db.Integer, db.ForeignKey("Point.id"), nullable = True)
    name = db.Column(db.String(255), nullable = False)
    summary = db.Column(db.String(255), nullable = False)
    description = db.Column(db.Text, nullable = False)
    difficulty = db.Column(db.String(9), nullable = False)
    location = db.Column(db.String(255), nullable = False)
    length = db.Column(db.Float, nullable = False)
    elevation_gain = db.Column(db.Integer, nullable = False)
    route_type = db.Column(db.String(15), nullable = False)
    
    # author = db.relationship("User", back_populates = "trails")
    starting_point = db.relationship("Point", foreign_keys = [starting_point_id])
    

class TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True
        sqla_session = db.session
        
    author_id = fields.Integer(required = True)
    
    # https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html
    @validates("route_type")
    def validate_route_type(self, value):
        valid_routes = ["Loop", "Out & back", "Point to point"]
        if value not in valid_routes:
            raise ValueError(f"Failed Route Type Validation: {value}. Must be in {valid_routes}")
        
          
class User(db.Model):
    __tablename__ = "User"
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String(255), nullable = False, unique = True)
    role = db.Column(db.String(6), nullable = False)
    
    trails = db.relationship(Trail, backref = "author")
    

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session