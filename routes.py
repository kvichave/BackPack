from flask import request, jsonify
from app import app, db
from models import LostItem, FoundItem
from datetime import datetime

@app.route("/lost-items/", methods=["POST"])
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


