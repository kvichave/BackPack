from flask import request, jsonify
from app import app, db
from models import LostItem, FoundItem,User
from datetime import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta


@app.route('/users/register', methods=['OPTIONS'])
def preflight():
    response = jsonify({"message": "Preflight OK"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    return response

@app.route("/users/register", methods=["POST"])
def register():
    data = request.json
    # response = jsonify({"message": "User registered successfully", "data": data})
    # response.headers.add("Access-Control-Allow-Origin", "*")  # Allow all origins
    # response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
    # response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "User already exists"}), 400
    user = User(username=data['username'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@app.route("/users/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
    return jsonify({"access_token": access_token}), 200



@app.route("/lost-items/", methods=["POST"])
@jwt_required()
def report_lost_item():
    data = request.json
    lost_item = LostItem(
        name=data["name"],
        description=data["description"],
        location=data["location"],
        date_lost=datetime.strptime(data["date_lost"], "%Y-%m-%d"),
        contact_info=data["contact_info"],
    )
    db.session.add(lost_item)
    db.session.commit()
    return jsonify({"message": "Lost item reported successfully"}), 201

@app.route("/found-items/", methods=["POST"])
@jwt_required()
def report_found_item():
    data = request.json
    found_item = FoundItem(
        name=data["name"],
        description=data["description"],
        location=data["location"],
        date_found=datetime.strptime(data["date_found"], "%Y-%m-%d"),
        contact_info=data["contact_info"],
    )
    db.session.add(found_item)
    db.session.commit()
    return jsonify({"message": "Found item reported successfully"}), 201


@app.route("/lost-items/", methods=["GET"])
def get_lost_items():
    lost_items = LostItem.query.all()
    return jsonify([{
        "id": item.id,
        "name": item.name,
        "description": item.description,
        "location": item.location,
        "date_lost": item.date_lost.strftime("%Y-%m-%d"),
        "contact_info": item.contact_info
    } for item in lost_items]), 200

@app.route("/found-items/", methods=["GET"])
def get_found_items():
    found_items = FoundItem.query.all()
    return jsonify([{
        "id": item.id,
        "name": item.name,
        "description": item.description,
        "location": item.location,
        "date_found": item.date_found.strftime("%Y-%m-%d"),
        "contact_info": item.contact_info
    } for item in found_items]), 200



@app.route("/match-items/", methods=["GET"])
def match_items():
    matches = []
    lost_items = LostItem.query.all()
    found_items = FoundItem.query.all()
    
    for lost in lost_items:
        for found in found_items:
            if lost.name.lower() == found.name.lower() and lost.location.lower() == found.location.lower():
                matches.append({
                    "lost_item": lost.name,
                    "found_item": found.name,
                    "location": lost.location,
                    "date_lost": lost.date_lost.strftime("%Y-%m-%d"),
                    "date_found": found.date_found.strftime("%Y-%m-%d"),
                    "contact_info": found.contact_info
                })
    
    return jsonify(matches), 200


@app.route("/lost-items/<int:id>", methods=["DELETE"])
def delete_lost_item(id):
    lost_item = LostItem.query.get(id)
    if not lost_item:
        return jsonify({"error": "Lost item not found"}), 404

    db.session.delete(lost_item)
    db.session.commit()
    return jsonify({"message": "Lost item removed successfully"}), 200

@app.route("/found-items/<int:id>", methods=["DELETE"])
def delete_found_item(id):
    found_item = FoundItem.query.get(id)
    if not found_item:
        return jsonify({"error": "Found item not found"}), 404

    db.session.delete(found_item)
    db.session.commit()
    return jsonify({"message": "Found item removed successfully"}), 200


