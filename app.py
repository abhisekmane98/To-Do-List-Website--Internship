
from flask import Flask, render_template, jsonify, request
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    unique_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    desc = db.Column(db.String(120), unique=False, nullable=False)
    schedule_date = db.Column(db.String(120), nullable=False,
                              default=datetime.utcnow)
    completion_date=db.Column(db.String(120), nullable=False,
                              default=datetime.utcnow)


@app.route("/add", methods=["GET", "POST"])
def add():
    lis = []
    data = request.get_json()
    print(data)
    title = data['title']
    desc = data['desc']
    schedule_date = data['scheduleDate']
    completion_date = data['completionDate']
    todo = Todo(title=title, desc=desc, schedule_date=schedule_date , completion_date=completion_date)
    db.session.add(todo)
    db.session.commit()
    TodoList = Todo.query.all()
    for todo in TodoList:
        lis.append({"unique_id": todo.unique_id, "title": todo.title, "desc": todo.desc,
                    "scheduleDate": todo.schedule_date,"completionDate":todo.completion_date})
    data = {
        "TodoList": lis
    }
    return jsonify(data)


@app.route("/delete/<int:id>/", methods=["GET", "POST"])
def deleteTodo(id):
    lis = []
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    TodoList = Todo.query.all()
    for todo in TodoList:
        lis.append({"unique_id": todo.unique_id, "title": todo.title, "desc": todo.desc,
                    "scheduleDate": todo.schedule_date,"completionDate":todo.completion_date})
    data = {
        "TodoList": lis
    }
    return jsonify(data)


@app.route("/show", methods=["GET", "POST"])
def show():
    lis = []
    TodoList = Todo.query.all()
    for todo in TodoList:
        lis.append({"unique_id": todo.unique_id, "title": todo.title, "desc": todo.desc,
                    "scheduleDate": todo.schedule_date,"completionDate":todo.completion_date})
    data = {
        "TodoList": lis
    }
    return jsonify(data)


@ app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, port=3000)
