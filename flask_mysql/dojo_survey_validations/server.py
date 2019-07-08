from flask import Flask, render_template, flash, request, redirect
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = "lomo_saltado"
# DATA SEEDING QUERIES
# insert into dojo_languages (language, created_at, updated_at) VALUES ('Python', NOW(), NOW())
# insert into dojo_languages (language, created_at, updated_at) VALUES ('JavaScript', NOW(), NOW())
# insert into dojo_languages (language, created_at, updated_at) VALUES ('Go', NOW(), NOW())
# insert into dojo_locations (location, created_at, updated_at) VALUES ('Seattle', NOW(), NOW())
# insert into dojo_locations (location, created_at, updated_at) VALUES ('San Jose', NOW(), NOW())

@app.route("/")
def index():
    mysql = connectToMySQL('dojo_survey_validations')
    query = "SELECT * FROM dojo_locations"
    locations = mysql.query_db(query)
    mysql = connectToMySQL('dojo_survey_validations')
    query = "SELECT * from dojo_languages"
    languages = mysql.query_db(query)
    return render_template("index.html", 
                           locations=locations, 
                           languages=languages)

@app.route("/survey", methods=['POST'])
def validate_survey():
    is_valid = True
    query = "INSERT INTO dojo_survey (name, dojo_languages_id, dojo_locations_id, comment, created_at, updated_at) VALUES (%(name)s, %(loc)s, %(fav_lang)s, %(comm)s, NOW(), NOW())"
    
    if len(request.form['location']) < 1:
        is_valid = False
        flash('Location cannot be blank')
    if len(request.form['name']) < 1:
        is_valid = False
        flash('Name cannot be blank')
    if len(request.form['language']) < 1:
        is_valid = False
        flash('Language cannot be blank')
    if len(request.form['comment']) > 120:
        is_valid = False
        flash('Comment cannot be more than 120 characters')

    if is_valid:
        data = {
            'name': request.form['name'],
            'loc': request.form['location'],
            'fav_lang': request.form['language'],
            'comm': request.form['comment']
        }
        mysql = connectToMySQL('dojo_survey_validations')
        survey_result_id = mysql.query_db(query, data)
        return redirect("/result/{}".format(survey_result_id))
    else:
        return redirect("/")     

@app.route("/result/<survey_id>")
def survey_result(survey_id):
    query = "SELECT * FROM dojo_survey JOIN dojo_languages ON dojo_survey.dojo_languages_id = dojo_languages.id JOIN dojo_locations on dojo_survey.dojo_locations_id = dojo_locations.id WHERE dojo_survey.id = %(id)s"
    data = {'id': survey_id}
    mysql = connectToMySQL('dojo_survey_validations')
    result = mysql.query_db(query, data)

    return render_template("result.html", survey_data = result[0])

if __name__ == "__main__":
    app.run(debug=True)