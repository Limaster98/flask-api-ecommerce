from models import User
from extensions import db, login_manager

# AUTENTICAÇÃO
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))