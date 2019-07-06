from flask import Flask, request, render_template, redirect
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/survey", methods=['POST'])
def result():
    return render_template("result.html", survey_data = request.form)

if __name__ == "__main__":
    app.run(debug=True)