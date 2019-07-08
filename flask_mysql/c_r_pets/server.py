from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL
app = Flask(__name__)
@app.route("/")
def index():
    mysql = connectToMySQL('cr_pets')	     
    pets = mysql.query_db('SELECT * FROM pets;')
    return render_template("index.html", saved_pets = pets)

@app.route("/add_pet", methods=['POST'])    
def commit_pet():
    mysql = connectToMySQL('cr_pets')	     
    query = "INSERT INTO pets (name, type, created_at, updated_at) VALUES (%(name)s, %(type)s, NOW(), NOW())"
    data = {
        'name': request.form['pet_name'],
        'type': request.form['pet_type']
    }
    mysql.query_db(query, data)       
    return redirect("/")  

if __name__ == "__main__":
    app.run(debug=True)