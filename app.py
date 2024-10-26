from flask import Flask, request, jsonify
from database import db
from models.user import User
from flask_login import LoginManager, login_user, current_user
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

login_manager = LoginManager()

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'


# View de autenticação/login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if data:
        username = data.get("username")
        password = data.get("password")
        if (username
                and password
                and len(password) >= 8
                and len(password) <= 10):
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return jsonify({"message": "Usuário cadastrado com sucesso"})
    return jsonify({"message": "Não foi possível cadastrar o usuário"}), 400


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if username and password:
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            print(current_user)
            return jsonify(
                {"message": "Autenticação realizada com sucesso"})
    return jsonify({"message": "Credenciais inválidas"}), 400


@app.route('/', methods=['GET'])
def hello_word():
    return '<h1>Hello world</h1>'


if __name__ == '__main__':
    app.run(debug=True)