from app import db
from flask_login import UserMixin
from app import login

class Utente(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    ruolo = db.Column(db.String(20), nullable=False)  # 'Amministrazione' o 'Gestore'

    def __repr__(self):
        return f'<Utente {self.username}>'

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)

class Scatola(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lotto = db.Column(db.String(50), nullable=False)
    data = db.Column(db.Date, nullable=False)
    numero_scatola = db.Column(db.Integer, nullable=False)
    prima_scelta = db.Column(db.Float, nullable=False)
    seconda_scelta = db.Column(db.Float, nullable=False)
    trosos = db.Column(db.Float, nullable=False)  # Nuova colonna
    scarti = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Scatola {self.numero_scatola} - Lotto {self.lotto} - {self.data}>'

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    vendite = db.relationship('Vendita', backref='cliente', lazy=True)

    def __repr__(self):
        return f'<Cliente {self.nome}>'

class Vendita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    data = db.Column(db.Date, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # 'Prima Scelta' o 'Seconda Scelta'
    peso = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Vendita {self.id} - Cliente {self.cliente.nome} - {self.data}>'

@login.user_loader
def load_user(id):
    return Utente.query.get(int(id))
