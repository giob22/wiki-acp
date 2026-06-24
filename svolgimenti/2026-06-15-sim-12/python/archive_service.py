from flask import Flask, request
from database import get_database

app = Flask(__name__)

db = get_database()

collection = db["pacchi"]

@app.errorhandler(415)
def unsupported_Media_Type(error):
    return {"Description": str(error.description)}, 415


@app.post("/archivia")
def archive():

    data = request.get_json()

    collection.insert_one(data)

    return {"Description": "TUTTO OK"}, 200




if __name__ == "__main__":
    app.run(debug=True)