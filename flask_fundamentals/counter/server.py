from flask import Flask, request, session, redirect, render_template
app = Flask(__name__)
app.secret_key = 'secret_keyy'

@app.route('/')
def landing():
    if "visits" not in session:
        session['visits'] = 0
    else:
        session['visits'] = session['visits'] + 1
    return render_template('index.html')

@app.route('/destroy_session')
def destroy_session():
    session.clear()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)