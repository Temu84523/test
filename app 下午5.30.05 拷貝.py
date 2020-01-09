from flask import Flask
import json
from flask import request
from flask import jsonify
app=Flask(__name__)

@app.route("/")
def home():
    return "hello dask"

@app.route("/port",methods=["POST"])
def test():
    data=request.get_json()
    name=data['name']
    return jsonify({"result":"success","name":name})

if __name__ == "__main__":
    app.run()