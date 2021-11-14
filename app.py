from logging import INFO
import re
from flask import Flask, app, render_template, make_response, jsonify, request

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'

Data = {
    "languages": {
        "en" : "English",
        "ar" : "Arabic",
    },
    "colors" : {
        "r" : "Red",
        "b" : "Blue",
    },
    "clouds" : {
        "AMAZON" : "AWS",
        "DIGITAL OCEAN" : "DO",
    }
}

@app.route("/")
def home():
    return "<h1 style='color-blue'> This is home!</h1>"


@app.route("/temp")
def template():
    return render_template("index.html")


@app.route("/qstr")
def query_string():
    if request.args:
        req = request.args
        res = {}
        for key, value in req.items():
            res[key] = value
        
        res = make_response(jsonify(res), 200)
        return res

    res = make_response(jsonify({"error" : "No query string"}), 400)
    return res


@app.route("/json")
def get_json():
    res = make_response(jsonify(Data), 200)
    return res


@app.route("/json/<collection>/<member>")
def get_data(collection, member):
    if collection in Data:
        member = Data[collection].get(member)
        if member:
            res = make_response(jsonify({"res": member}))
            return res

            res = make_response(jsonify({"error" : "No member found"}), 400)
            return res
    
    res = make_response(jsonify({"error" : "No collection found"}), 400)
    return res


@app.route("/json/<collection>", methods=["POST"])
def create_collection(collection):
    req = request.get_json()

    if collection in Data:
        res = make_response(jsonify({"error" : "Collections already exists"}))
        return res

    Data.update({collection: req})
    res = make_response({"message" : "Collection created"}, 201)
    return res

if __name__ == '__main__':
    print("Server running in port %s" %(PORT))
    app.run(host=HOST, port=PORT)