from flask import Flask, request, render_template, redirect, session
import random 
app = Flask(__name__)
app.secret_key = "torta"
@app.route("/")
def index():
    if 'server_number' not in session:
        session['server_number'] = random.randint(1, 100)
    return render_template("index.html")

@app.route("/guess", methods=['POST'])
def guess():
    user_guess = int(request.form['guess'])

    if user_guess >  session['server_number']:
        session['result'] = "too_high"
    elif user_guess < session['server_number']:
        session['result'] = "too_low"
    else:
        session['result'] = "got_it"
    return redirect("/")

@app.route('/play_again')
def play_again():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)