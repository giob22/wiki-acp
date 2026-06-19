from flask import Flask, request, abort
from pymongo import MongoClient
from utility import *

def get_collection():

    client = MongoClient("mongodb://localhost:27017")

    return (client["flotta"])["veicoli"]

collection = get_collection()



app = Flask(__name__)

@app.errorhandler(415)
def unsupported_media_type(e):
    return {"status": "Unsupported Media Type", "description": str(e.description)}, 415

@app.errorhandler(404)
def not_found(e):
    return {"status": "Not Found", "description": str(e.description)}, 404

@app.errorhandler(400)
def bad_request(e):
    return {"status": "Bad Request", "description": str(e.description)}, 400






@app.post(POST_REQUEST)
def updates():
    
    data = request.get_json()

    if data is None:
        abort(400)

    if data.get("vehicle_id") is None or data.get("battery") is None or  data.get("status") is None:
        abort(400)
    
    # cerco se è presente un document per tale veicolo

    document = collection.find_one({"vehicle_id":data.get("vehicle_id")})

    if document is None:
        # non esiste all'interno del database, lo devo inserire
        collection.insert_one(data)
    else:
        # significa che devo soltanto modificare il livello di batteria e lo stato

        collection.update_one({"vehicle_id":data.get("vehicle_id")},{"$set": {"status": data["status"], "battery": data["battery"]}})
    

    return {"status": "Success", "description": "Request fulfilled, document follows "}, 200

@app.get(GET_QUERY)
def searchs():
    try:
        params = request.query_string.decode("utf-8")
        data = params.split("=")
        if len(data) is not 2 or data[0] != "threshold":
            abort(400)
        threshold = int(data[1]) 
    except ValueError as e:
        abort(400, description=str(e))
    
    documents = list(collection.find({"$or": [{"status": "maintenance"}, {"battery":{"$lt": threshold}}]}))
    

    for document in documents:
        document["_id"] = str(document["_id"])
    

    return documents, 200



if __name__ == "__main__":
    print(f"DBserver avviato")
    app.run(debug=True)

