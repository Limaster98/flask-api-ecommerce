from flask import Flask #importando o flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)

#definir rota para a página inicial e a função que será executada quando for requisitado
@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == "__main__":      #verificar se esta rodando direto pelo main, evitando executar quando for importado
    app.run(debug=True)     #roda app com o debug ativo para auxiliar 