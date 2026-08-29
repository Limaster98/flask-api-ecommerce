from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import Product, User, CartItem

cart_routes = Blueprint('cart',__name__)

@cart_routes.route('/add/<int:product_id>',methods=['POST'])
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

@cart_routes.route('/remove/<int:product_id>', methods=['DELETE'])
@login_required
def remove_to_cart(product_id):
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()

    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'message':'Item removed from the cart succesfully'})
    return jsonify({'message':'Failed to remove item from the cart'}), 400

@cart_routes.route('/',methods=['GET'])
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

@cart_routes.route('/cart/checkout', methods=['POST'])
@login_required
def checkout():
    cart_items = current_user.cart
    for cart_item in cart_items:
        db.session.delete(cart_item)
    db.session.commit()
    return jsonify({'message':'Checkout succesful. Cart has been cleared'})