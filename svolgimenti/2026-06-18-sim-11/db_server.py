from pymongo import MongoClient
from flask import Flask, request, abort


app = Flask(__name__)

def get_collection():

    client = MongoClient("mongodb://localhost:27017")

    db = client["station_manager"]

    return db["trips"]


collection = get_collection()

@app.errorhandler(415)
def unsupported_media_type(e):
    return {"status": str(e.description)}, 415

@app.errorhandler(400)
def bad_request(e):
    return {"status": str(e.description)}, 400

@app.post("/update_history")
def update_history():

    data = request.get_json()

    if data.get("operation") is None or data.get("serial_number") is None:
        abort(400)

    print("data received: ", data)
    
    collection.insert_one(data)

    return {"status": "Success"}, 200

@app.get("/stats")
def stats():

    n_rents = collection.count_documents({"operation": "rent"})
    n_returns = collection.count_documents({"operation": "return"})


    return {"rent": n_rents,"return": n_returns}




if __name__ == "__main__":
    app.run(debug=True)