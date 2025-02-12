from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    # Add relationships
    lost_items = db.relationship('LostItem', backref='user', lazy=True)
    found_items = db.relationship('FoundItem', backref='user', lazy=True)

class LostItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    date_lost = db.Column(db.Date, nullable=False)
    contact_info = db.Column(db.String(100), nullable=False)
    image_filename = db.Column(db.String(255), nullable=True)
    # Add user relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class FoundItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    date_found = db.Column(db.Date, nullable=False)
    contact_info = db.Column(db.String(100), nullable=False)
    image_filename = db.Column(db.String(255), nullable=True)
    # Add user relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)