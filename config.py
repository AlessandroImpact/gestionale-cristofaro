import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Imposta la chiave segreta
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una-chiave-segreta-molto-difficile-da-indovinare'

    # Configura l'URI del database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    elif not SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

    # Disabilita il tracciamento delle modifiche (opzionale ma consigliato)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
