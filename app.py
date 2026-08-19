from flask import Flask, request, jsonify #importando o flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)

#modelagem do banco de dados, model:
#Produto (id, name, price, description)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)

#definir rota para a página inicial e a função que será executada quando for requisitado
@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/products/add', methods=["POST"]) #rota de adicionar produtos 
def add_product():
    data = request.json     #pega os dados enviados
    if 'name' in data and 'price' in data:      #verifica se os dados name e price estão preenchidos
        product = Product(name=data["name"], price=data["price"], description=data.get("description", ""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "Product added succesfully"})
    return jsonify({"message": "invalid product data"}), 400

@app.route('/products/delete/<int:product_id>', methods=["DELETE"]) #utilizamos <> para informar que iremos receber um dado e dentro qual será o tipo de dado
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"})
    return jsonify({"message": "Not found. Product not available"}), 404

if __name__ == "__main__":      #verificar se esta rodando direto pelo main, evitando executar quando for importado
    app.run(debug=True)     #roda app com o debug ativo para auxiliar 