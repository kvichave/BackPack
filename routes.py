from flask import request, jsonify,send_from_directory
from app import app, db
from models import LostItem, FoundItem,User
from datetime import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import time
import os


@app.route("/users/register", methods=["POST"])
def register():
    data = request.json
  
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
    access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=1))
    print(access_token)
    return jsonify({"access_token": access_token}), 200


@app.route("/lost-items/", methods=["POST"])
@jwt_required()
def report_lost_item():
    print(request.headers)  # Debugging line

    try:
        print("intry")
        # Get current user's ID from JWT token
        current_user_id = get_jwt_identity()
        print("aftertry")

        # Get form data
        name = request.form.get("name")
        description = request.form.get("description")
        location = request.form.get("location")
        date_lost = request.form.get("date_lost")
        contact_info = request.form.get("contact_info")
        
        # Handle image upload
        image = request.files.get('image')
        image_filename = None
        
        if image:
            filename = secure_filename(image.filename)
            image_filename = f"{int(time.time())}_{filename}"
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        # Create lost item with user_id
        lost_item = LostItem(
            name=name,
            description=description,
            location=location,
            date_lost=datetime.strptime(date_lost, "%Y-%m-%d"),
            contact_info=contact_info,
            image_filename=image_filename,
            user_id=current_user_id
        )
        
        db.session.add(lost_item)
        db.session.commit()
        
        return jsonify({"message": "Lost item reported successfully"}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route("/found-items/", methods=["POST"])
@jwt_required()
def report_found_item():
    current_user_id = get_jwt_identity()
    data = request.json
    found_item = FoundItem(
        name=data["name"],
        description=data["description"],
        location=data["location"],
        date_found=datetime.strptime(data["date_found"], "%Y-%m-%d"),
        contact_info=data["contact_info"],
        user_id=current_user_id
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
        "contact_info": item.contact_info,
        "image": f"http://localhost:5000/uploads/{item.image_filename}" if item.image_filename else None,
        "user_id": item.user_id,
        "reported_by": item.user.username
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
        "contact_info": item.contact_info,
        "user_id": item.user_id,
        "reported_by": item.user.username
    } for item in found_items]), 200

# Add routes to get items by user
@app.route("/my-lost-items/", methods=["GET"])
@jwt_required()
def get_my_lost_items():
    current_user_id = get_jwt_identity()
    lost_items = LostItem.query.filter_by(user_id=current_user_id).all()
    return jsonify([{
        "id": item.id,
        "name": item.name,
        "description": item.description,
        "location": item.location,
        "date_lost": item.date_lost.strftime("%Y-%m-%d"),
        "contact_info": item.contact_info,
        "image": f"http://localhost:5000/uploads/{item.image_filename}" if item.image_filename else None
    } for item in lost_items]), 200

@app.route("/my-found-items/", methods=["GET"])
@jwt_required()
def get_my_found_items():
    current_user_id = get_jwt_identity()
    found_items = FoundItem.query.filter_by(user_id=current_user_id).all()
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



@app.route('/nearby-lost-items', methods=['GET'])
def nearby_lost_items():
    location = request.args.get('location')
    items = LostItem.query.filter_by(location=location).all()
    return jsonify([{ "id": i.id, "description": i.description, "location": i.location, "date_lost": i.date_lost } for i in items])

@app.route('/lost-items/history', methods=['GET'])
@jwt_required()
def lost_items_history():
    user_id = get_jwt_identity()
    items = LostItem.query.filter_by(user_id=user_id).all()
    return jsonify([{ "id": i.id, "description": i.description, "location": i.location, "date": i.date } for i in items])

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


