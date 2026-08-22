from flask import Flask, request, jsonify #importando o flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = "MINHA_CHAVE_140198"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#modelagem do banco de dados, model:
#Produto (id, name, price, description)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)

#User (id, username, password)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    cart = db.relationship('CartItem', backref='user', lazy=True) 
    #criando relação do usuario com o carrinho
    #lazy=True é para que toda vez que precisamos consultar o usuario, não carregue sempre os dados do carrinho, só carregue caso solicitarmos para não perder performance

#CartItem(id, user_id, product_id)
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

# AUTENTICAÇÃO
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

#definir rota para a página inicial e a função que será executada quando for requisitado
@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/products/add', methods=["POST"]) #rota de adicionar produtos 
@login_required
def add_product():
    data = request.json     #pega os dados enviados
    if 'name' in data and 'price' in data:      #verifica se os dados name e price estão preenchidos
        product = Product(name=data["name"], price=data["price"], description=data.get("description", ""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "Product added succesfully"})
    return jsonify({"message": "invalid product data"}), 400

@app.route('/products/delete/<int:product_id>', methods=["DELETE"]) #utilizamos <> para informar que iremos receber um dado e dentro qual será o tipo de dado
@login_required
def delete_product(product_id):
    product = db.session.get(Product,product_id)    #product = Product.query.get(product_id) ESTE METODO QUERY.GET FICOU EM DESUSO, AGORA USAMOS SESSION.GET
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"})
    return jsonify({"message": "Not found. Product not available"}), 404

@app.route('/products/<int:product_id>', methods=["GET"]) #utilizamos <> para informar que iremos receber um dado e dentro qual será o tipo de dado
def get_product_detail(product_id):
    product = db.session.get(Product, product_id)
    if product:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        })
    return jsonify({"message": "Not found. Product not available"}), 404

@app.route('/products/update/<int:product_id>', methods=["PUT"]) #utilizamos <> para informar que iremos receber um dado e dentro qual será o tipo de dado
@login_required
def update_product(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({"message": "Not found. Product not available"}), 404
    data = request.get_json()
    if 'name' in data:
        product.name = data['name']
    if 'price' in data:
        product.price = data['price']
    if 'description' in data:
        product.description = data['description']
    db.session.commit()
    return jsonify({"message": "Product updated successfully"})

@app.route('/products',methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = []
    for product in products:
        product_list.append({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        })
    return jsonify(product_list)

@app.route('/login', methods=['POST'])
def login():
    login_data = request.json
    user = User.query.filter_by(username=login_data.get('username')).first()
    if user and user.password == login_data.get('password'):
        login_user(user)
        return jsonify({"message": "Logged in successfully"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout succesfully"})

if __name__ == "__main__":      #verificar se esta rodando direto pelo main, evitando executar quando for importado
    app.run(debug=True)     #roda app com o debug ativo para auxiliar 