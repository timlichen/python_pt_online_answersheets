from flask import Flask, request, render_template, redirect, session
import random 
app = Flask(__name__)
app.secret_key = "torta"
@app.route("/")
def index():
    if 'server_number' not in session:
        session['server_number'] = random.randint(1, 100)
        print(session['server_number'])
    if 'attempt' not in session:
        session['attempt'] = 0
    if 'winners' not in session:
        session['winners'] = {}
    
    return render_template("index.html")

@app.route("/guess", methods=['POST'])
def guess():    
    user_guess = int(request.form['guess'])
    session['attempt'] = session['attempt'] + 1

    if session['attempt'] == 5:
        session['result'] = "you_lose"
    elif user_guess >  session['server_number']:
        session['result'] = "too_high"
    elif user_guess < session['server_number']:
        session['result'] = "too_low"
    else:
        session['result'] = "got_it"
    return redirect("/")

@app.route('/play_again')
def play_again():
    session.pop('attempt')
    session.pop('server_number')
    session.pop('result')
    return redirect("/")

@app.route("/leader_board", methods=['POST'])
def leader_board():
    session['winners']
    session['winners'][request.form['name']] = session['attempt']
    session.modified = True
    print(session['winners'])
    return redirect ("/")

@app.route("/board")
def show_leaders():
    return render_template('leader_board.html')

if __name__ == "__main__":
    app.run(debug=True)