from flask import Flask, request, abort
import http



import logging

app = Flask(__name__)


logger = logging.getLogger("TICKET_SERVER")
print = logger.info

sales = {"EVT-A": 0, "EVT-B": 0, "EVT-C": 0}

@app.errorhandler(415)
def on_json_loading_failed(e):
    return ({"status": str(e.name),"description": str(e.description)}, 415)

@app.errorhandler(400)
def on_bad_request(e):
    return ({"status": str(e.name),"description": str(e.description)}, 415)


@app.post("/sale")
def sale():
    
    data = request.get_json()

    if data.get("event_id") is None or data.get("qty") is None:
        abort(400) 

    sales[data["event_id"]] += data["qty"]

    with open("./sales.log", mode="a") as file:
        file.write(f"{data["event_id"]}|{data["qty"]}\n")
    

    return {"status": "reserve registred"}

@app.get("/report")
def report():
    return sales, 200
    
    




if __name__ == "__main__":
    app.run(debug=True)