from flask import Flask #importando o flask

app = Flask(__name__)

#definir rota para a página inicial e a função que será executada quando for requisitado
@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == "__main__":      #verificar se esta rodando direto pelo main, evitando executar quando for importado
    app.run(debug=True)     #roda app com o debug ativo para auxiliar 