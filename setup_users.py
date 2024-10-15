from app import app, db
from app.models import Utente

def create_users():
    with app.app_context():
        # Elimina eventuali utenti esistenti con gli stessi username
        Utente.query.filter_by(username='Amministrazione').delete()
        Utente.query.filter_by(username='Gestore').delete()
        db.session.commit()

        # Creare l'utente Amministrazione
        admin = Utente(username='Amministrazione', ruolo='Amministrazione')
        admin.set_password('Trufas2024')

        # Creare l'utente Gestore
        gestore = Utente(username='Gestore', ruolo='Gestore')
        gestore.set_password('Trufas2024')

        # Aggiungere gli utenti al database
        db.session.add(admin)
        db.session.add(gestore)
        db.session.commit()
        print('Utenti creati con successo.')

if __name__ == '__main__':
    create_users()
