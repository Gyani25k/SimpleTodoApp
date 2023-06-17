from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuration for connecting to the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    # Model for representing a todo item
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route("/")
def home():
    # Home route to display the todo list
    if 'username' in session:
        # If the user is logged in, retrieve all todo items from the database
        todo_list = Todo.query.all()
        return render_template("base.html", todo_list=todo_list)
    else:
        # If the user is not logged in, redirect to the login page
        return redirect(url_for("login"))


@app.route("/add", methods=["POST"])
def add():
    # Route for adding a new todo item
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    # Route for updating the status of a todo item
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    # Route for deleting a todo item
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/login", methods=["GET", "POST"])
def login():
    # Route for handling user login
    if request.method == "POST":
        # If the request method is POST, process the login form data
        username = request.form.get("username")
        password = request.form.get("password")

        # Your authentication logic goes here
        if username == "admin" and password == "password":
            # If the username and password are correct, store the username in the session
            session['username'] = username
            return redirect(url_for("home"))
        else:
            # If the username or password is incorrect, show an error message
            return render_template("login.html", error="Invalid credentials")
    else:
        # If the request method is GET, render the login form
        return render_template("login.html", error="")


@app.route("/logout")
def logout():
    # Route for handling user logout
    session.pop('username', None)
    return redirect(url_for("home"))


if __name__ == "__main__":
    with app.app_context():
        # Create the database tables if they don't exist
        db.create_all()
    app.run(debug=True)
