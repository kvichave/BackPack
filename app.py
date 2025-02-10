from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend interactions

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lost_found.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import routes (to avoid circular imports)
from routes import *

if __name__ == "__main__":
    app.run(debug=True)
