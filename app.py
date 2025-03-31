from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)   #Initializes the Flask application.
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db" #Configures SQLite as the database (todo.db will be created).
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False  #Disables modification tracking for performance.
db=SQLAlchemy(app)  #creating a database

class Todo(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"{self.Sno} - {self.title}"

@app.route("/", methods= [ 'GET', 'POST'])
def home():
    if request.method=="POST":
        title=request.form["title"]
        desc=request.form["desc"]
        todo=Todo(title = title, desc = desc)
        db.session.add(todo)    #to add
        db.session.commit()     #to commit
        return redirect("/")
        
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo )

@app.route("/about")
def about():
    return render_template("about.html")  # Renders the about page

@app.route("/update/<int:Sno>", methods= [ 'GET', 'POST'])
def update(Sno):
    if request.method=='POST':
        title=request.form["title"]
        desc=request.form["desc"]
        todo = Todo.query.filter_by(Sno=Sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)    #to add
        db.session.commit()     #to commit
        return redirect("/")

    todo = Todo.query.filter_by(Sno=Sno).first()
    return render_template('update.html', todo=todo )

@app.route("/delete/<int:Sno>")
def delete(Sno):  
    todo = Todo.query.filter_by(Sno=Sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route("/search")
def search():
    query = request.args.get("query", "").strip()
    if query:
        results = Todo.query.filter(Todo.title.contains(query) | Todo.desc.contains(query)).all()
    else:
        results = []

    return render_template("search.html", results=results, query=query)

if __name__=="__main__":
    app.run(debug=True, port=9000)