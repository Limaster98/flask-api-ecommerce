from flask import Flask, request, jsonify #importando o flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

application = Flask(__name__)
application.config['SECRET_KEY'] = "MINHA_CHAVE_140198"
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(application)
login_manager = LoginManager()
login_manager.init_app(application)
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
@application.route('/')
def hello_world():
    return 'Hello World!'

@application.route('/products/add', methods=["POST"]) #rota de adicionar produtos 
@login_required
def add_product():
    data = request.json     #pega os dados enviados
    if 'name' in data and 'price' in data:      #verifica se os dados name e price estão preenchidos
        product = Product(name=data["name"], price=data["price"], description=data.get("description", ""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "Product added succesfully"})
    return jsonify({"message": "invalid product data"}), 400

@application.route('/products/delete/<int:product_id>', methods=["DELETE"]) #utilizamos <> para informar que iremos receber um dado e dentro qual será o tipo de dado
@login_required
def delete_product(product_id):
    product = db.session.get(Product,product_id)    #product = Product.query.get(product_id) ESTE METODO QUERY.GET FICOU EM DESUSO, AGORA USAMOS SESSION.GET
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"})
    return jsonify({"message": "Not found. Product not available"}), 404

@application.route('/products/<int:product_id>', methods=["GET"]) #utilizamos <> para informar que iremos receber um dado e dentro qual será o tipo de dado
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

@application.route('/products/update/<int:product_id>', methods=["PUT"]) #utilizamos <> para informar que iremos receber um dado e dentro qual será o tipo de dado
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

@application.route('/products',methods=['GET'])
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

@application.route('/login', methods=['POST'])
def login():
    login_data = request.json
    user = User.query.filter_by(username=login_data.get('username')).first()
    if user and user.password == login_data.get('password'):
        login_user(user)
        return jsonify({"message": "Logged in successfully"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@application.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout succesfully"})

@application.route('/cart/add/<int:product_id>',methods=['POST'])
@login_required
def add_to_cart(product_id):
    user = db.session.get(User,current_user.id)
    product = db.session.get(Product,product_id)

    if user and product:
        cart_item = CartItem(user_id=user.id, product_id=product.id)
        db.session.add(cart_item)
        db.session.commit()
        return jsonify({'message':'Item added to the cart succesfully'})
    
    return jsonify({'message':'Failed to add item to the cart'}),400

@application.route('/cart/remove/<int:product_id>', methods=['DELETE'])
@login_required
def remove_to_cart(product_id):
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()

    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'message':'Item removed from the cart succesfully'})
    return jsonify({'message':'Failed to remove item from the cart'}), 400

@application.route('/cart',methods=['GET'])
@login_required
def get_cart():
    cart_itens = current_user.cart
    cart_item_list = []
    if cart_itens:
        for cart_item in cart_itens:
            product = db.session.get(Product,cart_item.product_id)
            cart_item_list.append({
                'id': cart_item.id,
                'user_id': cart_item.user_id,
                'product_id': cart_item.product_id,
                'product_name': product.name,
                'product_price': product.price
            })
    return jsonify(cart_item_list)

@application.route('/cart/checkout', methods=['POST'])
@login_required
def checkout():
    cart_items = current_user.cart
    for cart_item in cart_items:
        db.session.delete(cart_item)
    db.session.commit()
    return jsonify({'message':'Checkout succesful. Cart has been cleared'})

if __name__ == "__main__":      #verificar se esta rodando direto pelo main, evitando executar quando for importado
    application.run(debug=True)     #roda application com o debug ativo para auxiliar 