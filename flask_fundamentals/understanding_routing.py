from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World"

@app.route('/dojo')
def dojo():
    return "Dojo"

@app.route('/say/<name>')
def say_name(name):
    if type(name) == str:
        return "Hi {}".format(name)
    else:
        return "Strings Only"

@app.route('/repeat/<num>/<word>')
def repeat(num, word):
    if num.isdigit() and type(word) == str: 
        return word * int(num)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return 'Sorry! No response. Try again.'

if __name__ == '__main__':
    app.run(debug=True)