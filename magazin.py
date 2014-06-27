import flask

app=flask.Flask(__name__)

@app.route('/')
def home():
	return flask.render_template('home.html')

@app.route('/save')
def save():
    print "saving..."
    return 'ok'

app.run(debug=True)

