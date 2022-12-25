from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

    d = datetime.now()
    timezone = pytz.timezone("Asia/Kolkata")
    d_aware = timezone.localize(d)

    date_created = db.Column(db.DateTime, default=d)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<Task %r>" % self.id


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        task_content = request.form["content"].strip()
        new_task = Todo(content=task_content[:25])

        if len(task_content) > 2:
            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect("/")
            except:
                return "There was an issue adding your task"
        else:
            return redirect("/")

    else:
        tasks = Todo.query.order_by(Todo.completed).all()
        return render_template("index.html", tasks=tasks)


@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting that task"


@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    task = Todo.query.get_or_404(id)

    task.content = request.json["content"]

    try:
        db.session.commit()
        return redirect("/")
    except:
        return "There was an issue updating your task"


@app.route("/complete/<int:id>")
def complete(id):
    task = Todo.query.get_or_404(id)

    task.completed = True

    try:
        db.session.commit()
        return redirect("/")
    except:
        return "There was an issue updating your task"


@app.route("/incomplete/<int:id>")
def incomplete(id):
    task = Todo.query.get_or_404(id)

    task.completed = False

    try:
        db.session.commit()
        return redirect("/")
    except:
        return "There was an issue updating your task"


@app.route("/clearcomp")
def clearcomp():
    Todo.query.filter_by(completed=True).delete()

    try:
        db.session.commit()
        return redirect("/")
    except:
        return "There was an issue updating your task"


@app.route("/showpend")
def showpend():
    tasks = Todo.query.order_by(Todo.completed).filter(Todo.completed == False).all()
    return render_template("index.html", tasks=tasks)


@app.route("/showcomp")
def showcomp():
    tasks = Todo.query.order_by(Todo.completed).filter(Todo.completed == True).all()
    return render_template("index.html", tasks=tasks)


if __name__ == "__main__":
    app.run()
