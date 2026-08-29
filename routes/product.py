from flask import Blueprint, request, jsonify
from flask_login import login_required
from extensions import db
from models import Product

products_route = Blueprint('products',__name__)

@products_route.route('/add', methods=["POST"]) #rota de adicionar produtos 
@login_required
def add_product():
    data = request.json     #pega os dados enviados
    if 'name' in data and 'price' in data:      #verifica se os dados name e price estão preenchidos
        product = Product(name=data["name"], price=data["price"], description=data.get("description", ""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "Product added succesfully"})
    return jsonify({"message": "invalid product data"}), 400

@products_route.route('/delete/<int:product_id>', methods=["DELETE"]) #utilizamos <> para informar que iremos receber um dado e dentro qual será o tipo de dado
@login_required
def delete_product(product_id):
    product = db.session.get(Product,product_id)    #product = Product.query.get(product_id) ESTE METODO QUERY.GET FICOU EM DESUSO, AGORA USAMOS SESSION.GET
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"})
    return jsonify({"message": "Not found. Product not available"}), 404

@products_route.route('/<int:product_id>', methods=["GET"]) #utilizamos <> para informar que iremos receber um dado e dentro qual será o tipo de dado
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

@products_route.route('/update/<int:product_id>', methods=["PUT"]) #utilizamos <> para informar que iremos receber um dado e dentro qual será o tipo de dado
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

@products_route.route('/',methods=['GET'])
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