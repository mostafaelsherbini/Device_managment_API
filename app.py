import json
from flask import Flask, request , jsonify 

app = Flask(__name__)

notes = [
{
    "id" : 4,
    "note" : "hey Are you okay"
}

]
@app.route("/")
def home():
    return "welcome"

@app.route("/notes")
def note():
    return notes


# Get
@app.route("/get",methods=['GET'])
def Get():
    data = request.get_json()
    if not data or 'id' not in data:
        return 400
    for id in notes:
        if data['id'] == id['id']:
            return id 
    return "not found"
            

#Post
@app.route("/add_note" , methods=['POST'])
def add_note():
    
    data = request.get_json()
    if not data or 'note' not in data:
        return jsonify({"error": "Bad Request", "message": "Missing 'name' field"}), 400

    new_note = {
        "id" : len(notes) + 1,
        "note" : data['note']
    }

    notes.append(new_note)
    return jsonify(new_note), 201


@app.route('/delete', methods=['DELETE'])
def delete():
    data = request.get_json()

    if not data or 'id' not in data:
        return 400
    for id in notes:
        if data['id'] == id['id']:
            notes.remove(id)
            return "Done"
    else:
        return "not found"


@app.route('/update' , methods=['PATCH'])
def update():
    data = request.get_json()
    if not data or "id" and "note" not in data:
        return 400
    for index , i in enumerate(notes):
        if data["id"] == i["id"]:
            notes[index] = {
                "id": i['id'],
                "note": data['note']
            }
        return "Done"
    else:
        return "not found"

if __name__ == "__main__":
    app.run(debug=True)


