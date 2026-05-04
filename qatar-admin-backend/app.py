from flask import Flask
from config import Config
from extensions import db, bcrypt, login_manager
from routes.auth import auth
from routes.opportunities import opportunity
from flask_cors import CORS
from models import Admin

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
CORS(app, supports_credentials=True)

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(opportunity, url_prefix="/opportunities")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
