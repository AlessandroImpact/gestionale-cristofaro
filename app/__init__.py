from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

from app import routes, models

# Funzioni di utilità per i template
@app.context_processor
def utility_processor():
    def calculate_total_weight_scatole(items):
        return sum(item.prima_scelta + item.seconda_scelta + item.scarti for item in items)
    def calculate_total_weight_vendite(vendite):
        return sum(vendita.peso for vendita in vendite)
    return dict(
        calculate_total_weight_scatole=calculate_total_weight_scatole,
        calculate_total_weight_vendite=calculate_total_weight_vendite
    )
