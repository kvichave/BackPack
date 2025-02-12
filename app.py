from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
app.config['JWT_SECRET_KEY'] = 'supersecretkey'  
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lost_found.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

jwt = JWTManager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)





from routes import *

if __name__ == "__main__":
    with app.app_context():
            db.create_all()
    app.run(debug=True, port=5000)