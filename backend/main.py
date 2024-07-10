from flask import request, jsonify
from config import app, db  
from models import Contact
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
secret_id = os.getenv("CLIENT_SECRET")

def get_token() :
    auth_string = client_id + ":" + secret_id
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {"grant_type" : "client_credentials"}
    result = post(url,headers=headers,data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token) :
    return {"Authorization": "Bearer " + token}

def search_for_artist(token,artist_name) :
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"q={artist_name}&type=artist&limit=1"
    
    query_url = url + "?" + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0 :
        return None
    
    return json_result[0]

def get_songs_by_artist(token,artist_id) :
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

token = get_token()

@app.route("/contacts",methods=["GET"])
def get_contacts():
    contacts = Contact.query.all()
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    return jsonify({"contacts": json_contacts})

@app.route("/create_contact", methods=["POST"])
def create_contacts() :
   
    delete_contact()
    
    artist = request.json.get("artist")
    
    if not artist :
        return jsonify({"message": "you must include a valid artist name"}), 400
    
    result = search_for_artist(token, artist)
    artist_id = result["id"]
    songs = get_songs_by_artist(token, artist_id)
    
    for i,track in enumerate(songs) :
        new_contact = Contact(track=track['name'])
        try: 
            db.session.add(new_contact)
            db.session.commit()
        except Exception as e:
             return jsonify({"message": str(e)}), 400
    
    return jsonify({"message": "top tracks found"}), 201
    
    
@app.route("/update_contact/<int:user_id>") 
def update_contact() :
    delete_contact()
    create_contacts()
    

@app.route("/delete_contact/<int:user_id>")
def delete_contact() :
    user_id = 1
    contact = Contact.query.get(user_id)
    while contact :
        db.session.delete(contact)
        db.session.commit()
        user_id += 1
        contact = Contact.query.get(user_id)
    
    return jsonify({"message" : "user deleted"}), 200
if __name__ == "__main__" :
    with app.app_context() :
        db.create_all()
        
    app.run(debug=True, port=8888)