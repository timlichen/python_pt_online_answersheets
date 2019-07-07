from flask import Flask, render_template, request, session, redirect
import random
from datetime import datetime
app = Flask(__name__)
app.secret_key = "burrito"
@app.route("/")
def ninja_gold():
    if 'gold' not in session:
        session['gold'] = 0
    if 'activites' not in session:
        session['activites'] = []
    if 'attempts' not in session:
        session['attempts'] = 0
    return render_template("index.html")

@app.route('/process_money', methods=['POST'])
def process_money():

    if session['attempts'] < 15:
        session['attempts'] += 1    
        gold_ranges = {'farm': [10,20],
                       'cave': [5, 10],
                       'house': [2, 5],
                       'casino': [-50, 50]
                       }
                       
        gold = random.randint(gold_ranges[request.form['building']][0],
                              gold_ranges[request.form['building']][1])    

        session['gold'] += gold 

        # if request.form['building'] == 'farm':
        #     gold = random.randint(10, 20)
        #     session['gold'] += gold

        # elif request.form['building'] == 'cave':
        #     gold = random.randint(5, 10)
        #     session['gold'] += gold

        # elif request.form['building'] == 'house':
        #     gold = random.randint(2, 5)
        #     session['gold'] += gold

        # elif request.form['building'] == 'casino':
        #     gold = random.randint(-50, 50)
        #     session['gold'] += gold
        
        if gold >= 0:
            session['activites'].insert(0, ["Earned {} golds from the {} : {}".format(gold, request.form['building'], datetime.now()), True])
        else:
            session['activites'].insert(0, ["Earned {} golds from the {} : {}".format(gold, request.form['building'], datetime.now()), False])
    else:
        if session['gold'] > 500:
            session['result'] = "Winner"
        else:
            session['result'] = "Loser"

    return redirect("/")

@app.route('/restart_game')
def restart_game():
    session.clear()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)