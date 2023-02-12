from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.app_context().push()

# /// = relative path, //// = absolute path
# local db configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Class definition for each todo, which has an id, title, and bool indicator of completeness.
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

#Routing, our HTML uses the paths like "/", "/add", etc. to call this file and complete corresponding actions, like all those below.
@app.route("/")
def home():
    # querying for all todos in db
    todo_list = Todo.query.all()
    #Props - Somewhat similar as in Svelte, but instead we pass props as data from our db into our template rather than some 'child' component.
    return render_template("base.html", todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    # creation of new todo object
    new_todo = Todo(title=title, complete=False)
    # inserting todo into db
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))

#DynamicURLs, we can insert variables into the URL that we can use them as arguments to the function corresponding to a route,
# such as here where we use the id of a todo to know which one to update.
@app.route("/update/<int:todo_id>")
def update(todo_id):
    # db query for todo by the id passed in route url
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)