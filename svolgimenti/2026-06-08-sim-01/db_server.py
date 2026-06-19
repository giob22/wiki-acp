from flask import Flask, request
from utility import logging
import database

logger = logging.getLogger("DB_SERVER")

db = database.get_database()

collection = db['readings']

db_server = Flask(__name__)

def create_response(description, status_code):
    return ({"result": description}, status_code)



@db_server.post("/readings")
def readings():
    try:
        payload = request.get_json()

        logger.info(f"payload ricevuto:\n{payload}")

        collection.insert_one(payload)

        logging.info("payload del messaggio inserito all'interno del database")
        return create_response("operazione avvenuta con successo", 200)
    except Exception as e:
        logger.info(e)
        return create_response("operazione non riuscita", 500)

@db_server.get("/stats")
def stats():

    cursor = collection.find({})

    list_readings = list(cursor)

    statistiche = {}
    n_media = {}

    logging.info(list_readings)

    for r in list_readings:
        if r.get("location") in statistiche.keys() and r.get("temperature") is not None:
            statistiche[r.get("location")] += r.get("temperature")
            n_media[r.get("location")] += 1
        elif r.get("location") is None or  r.get("temperature") is  None:
            return create_response("il database non è consistente", 500)
        else:
            statistiche[r.get("location")] = r["temperature"]
            n_media[r.get("location")] = 1
    
    for location in statistiche.keys():
        statistiche[location] = statistiche[location] / n_media[location]
    # PROVA AD UTILIZZARE QUESTO
    # pipeline = [
    #     {'$group': {'_id': '$location',
    #                 'avg_temperature': {'$avg': '$temperature'}
    #                 }
    #             },
    #             {'$project': {'$_id': "location",
    #                           '$avg_temperature': 1}}
    # ]

    
        

    return statistiche, 200






if __name__ == "__main__":
    db_server.run(debug=True)

