from flask import Flask, render_template
app = Flask(__name__)

# level 1 - render 3 boxes
@app.route('/play')
def index():
    return render_template('index.html', num_times=3)

# level 2 - render x boxes
@app.route('/play/<num>')
def play(num):
    return render_template('index.html', num_times=int(num))

# level 3 - render x boxes of given color
@app.route('/play/<num>/<color>')
def color(num, color):
    return render_template('index.html', num_times=int(num), color=color)

if __name__=="__main__":
    app.run(debug=True)