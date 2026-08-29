from flask import Flask, jsonify #importando o flask
from routes.product import products_route
from routes.user import users_route
from routes.cart import cart_routes
from extensions import db, login_manager
from models import User

application = Flask(__name__)
application.config['SECRET_KEY'] = "MINHA_CHAVE_140198"
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
db.init_app(application)

login_manager.init_app(application)
login_manager.login_view = 'login'

# AUTENTICAÇÃO
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

application.register_blueprint(products_route, url_prefix='/products')
application.register_blueprint(users_route, url_prefix='/user')
application.register_blueprint(cart_routes,  url_prefix='/cart')

#definir rota para a página inicial e a função que será executada quando for requisitado
@application.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == "__main__":      #verificar se esta rodando direto pelo main, evitando executar quando for importado
    application.run(debug=True)     #roda application com o debug ativo para auxiliar 