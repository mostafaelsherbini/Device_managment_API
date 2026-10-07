import json 
from flask import Flask , request , jsonify 
import sqlite3

app = Flask(__name__)


def Db():
    db=get_db()
    cr = db.cursor()
    cr.execute("select * from devices")
    data_base = cr.fetchall()
    return data_base


def get_db():
    return sqlite3.connect("devices.db")



# create the tables and fieleds 
db = get_db()
cr = db.cursor()
cr.execute("Create Table if not exists  devices (name text,id ineger,type text,status text)")

@app.route('/')
def home():
    return "welcome to Device_managment"


@app.route('/devices', methods=['GET'])
def get_all():
    db = get_db()
    cr = db.cursor()
    cr.execute("select * from devices")
    data_base = cr.fetchall()
    return jsonify(data_base)

@app.route('/devices/<int:id>/', methods=['GET'])
def get_device(id):
    for i in Db():
        if i[1] == id :
            return jsonify(i) #flask (Rest APIs in python) doesn't accept 'tuple' as a return data
        
    return "not found"

#Inserting the data 
@app.route('/create_device', methods=['POST'])
def create_device():
    db = get_db()
    cr = db.cursor()
    data = request.get_json()
    if not data or 'name' not in data:
        return "No data" , 400
    cr.execute("select * from devices")
    id_num = cr.fetchall()
    cr.execute(f"""insert into devices(name,id,type,status) 
               values('{data['name']}',{id_num[-1][1]+1}, '{data['type']}','{data['status']}')    """)
    db.commit()
    db.close()
    return "done" 


#update data
@app.route('/update', methods=['PATCH'])
def update():
    db = get_db()
    cr = db.cursor()
    data = request.get_json()
    if not data or not 'name' in data:
        return "data not found" 
    cr.execute(f"update devices set status = '{data['status']}' where name ='{data['name']}' ")
    db.commit()
    return "done"

 

#Delete data
@app.route("/delete/<int:id>", methods=['DELETE'])
def delete(id):
    db = get_db()
    cr = db.cursor()
    cr.execute(f"delete from devices where id = {id}")
    db.commit()
    return "done"



if __name__ == "__main__":
   app.run(debug=True)
