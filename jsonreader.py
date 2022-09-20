from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import or_, and_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= "mysql+pymysql://root:123tama@34.102.24.145/logreg"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(30))
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

db.create_all()

class UserSchema(ma.Schema):
    class meta:
        fields = ('id','username', 'password')
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/reg_usr', methods=['POST'])
def createuser():
    username = request.json['user']
    password = request.json['password']
    new_user= Users(username, password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "usuario creado"})

@app.route('/del_usr', methods=['POST'])
def deleteuser():
    username_json = request.json['user']
    db.session.query(Users).filter(Users.username == username_json).delete()
    db.session.commit()
    return jsonify({"message":"usuario eliminado"})
 

@app.route('/val_usr', methods=['POST'])
def checkeuser():
    username_json = request.json['user']
    password_json = request.json['password']

    check_query = db.session.query(Users).filter(and_(Users.username == username_json,
    Users.password == password_json))
    db.session.commit()
    result_list = check_query.all()
    rows = len(result_list)
    print(rows)
    
    if (rows > 0):
          return jsonify({"message":"ya registrado"})
    else:
        return jsonify({"message":"no se encuentra registrado"})
      

if __name__ == '__main__':
    app.run(debug=True)
