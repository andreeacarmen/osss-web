import flask
from flask.ext.sqlalchemy import SQLAlchemy

app=flask.Flask(__name__)
app.config['SECRET_KEY']='ceva secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/student/osss-web/db.sqlite'
db=SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)

@app.route('/')
def home():
	return flask.render_template('home.html', product_list=Product.query.all())

@app.route('/save', methods=['POST'])
def save():
    print "saving...", flask.request.form['name']
    product = Product(name=flask.request.form['name'])
    db.session.add(product)
    db.session.commit()
    flask.flash("produs salvat")
    return flask.redirect('/')

@app.route('/edit/<int:product_id>', methods=['POST', 'GET'])
def edit(product_id):
    product = Product.query.get(product_id)
    if not product:
        flask.abort(404)
    if flask.request.method == 'POST':
        product.name = flask.request.form['name']
        db.session.commit()
        return flask.redirect('/')
    return flask.render_template('edit.html', product=product)

@app.route('/api/list')
def api_list():
    product_id_list = []
    for product in Product.query.all():
        product_id_list.append(product.id)
    return flask.jsonify({
        'id_list':product_id_list
    })

@app.route('/api/product/<int:product_id>')
def api_product(product_id):
    product=Product.query.get(product_id)
    return flask.jsonify({
        'id':product.id,
        'name':product.name,
    })

db.create_all()
app.run(debug=True)

