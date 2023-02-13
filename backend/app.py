from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/db_flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text())
    date = db.Column(db.DateTime, default=datetime.datetime.now)

    
    def __init__(self, title, body):
        self.title = title
        self.body = body


class NoteSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'body', 'date')
        

note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)


@app.route('/get', methods=['GET'])
def get_note():
    all_notes = Notes.query.all()
    result = notes_schema.dump(all_notes)
    return jsonify(result)


@app.route('/get/<id>/', methods=['GET'])
def post_details(id):
    note = Notes.query.get(id)
    return note_schema.jsonify(note)


@app.route('/add', methods=['POST'])
def add_note():
    title = request.json['title']
    body = request.json['body']

    notes = Notes(title, body)
    db.session.add(notes)
    db.session.commit()
    return note_schema.jsonify(notes)


@app.route('/update/<id>/', methods=['PUT'])
def update_note(id):
    note = Notes.query.get(id)
    
    title = request.json['title']
    body = request.json['body']
    
    note.title = title
    note.body = body
    
    db.session.commit()
    return note_schema.jsonify(note)

@app.route('/delete/<id>/', methods = ['DELETE'])
def note_delete(id):
    note = Notes.query.get(id)
    
    db.session.delete(note)
    db.session.commit()
    
    return note_schema.jsonify(note)


if __name__ == "__main__":
    app.run(debug=True)
