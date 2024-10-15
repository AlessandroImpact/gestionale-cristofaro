from app import app, db
from flask import render_template, redirect, url_for, request, flash
from app.models import Scatola, Cliente, Vendita, Utente
from datetime import datetime, timedelta
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import func, desc
from werkzeug.security import generate_password_hash, check_password_hash

# Rotta per la pagina di login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        utente = Utente.query.filter_by(username=username).first()
        if utente is None or not utente.check_password(password):
            flash('Credenciales inválidas. Por favor, inténtelo de nuevo.')
            return redirect(url_for('login'))
        login_user(utente)
        return redirect(url_for('home'))
    return render_template('login.html')

# Rotta per il logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Rotta per la home page
@app.route('/')
@login_required
def home():
    scatole = Scatola.query.order_by(Scatola.data.desc()).all()
    return render_template('home.html', scatole=scatole)

# Rotta per inserire una nuova scatola
@app.route('/inserisci', methods=['GET', 'POST'])
@login_required
def inserisci():
    if request.method == 'POST':
        lotto = request.form['lotto']
        data = datetime.strptime(request.form['data'], '%Y-%m-%d')
        numero_scatola = int(request.form['numero_scatola'])
        prima_scelta = float(request.form['prima_scelta'])
        seconda_scelta = float(request.form['seconda_scelta'])
        trosos = float(request.form['trosos'])  # Nuovo campo
        scarti = float(request.form['scarti'])
        scatola = Scatola(
            lotto=lotto,
            data=data,
            numero_scatola=numero_scatola,
            prima_scelta=prima_scelta,
            seconda_scelta=seconda_scelta,
            trosos=trosos,  # Nuovo campo
            scarti=scarti
        )
        db.session.add(scatola)
        db.session.commit()
        flash('Caja insertada con éxito.')
        return redirect(url_for('home'))
    return render_template('inserisci.html')

# Rotta per eliminare una scatola
@app.route('/elimina_scatola/<int:scatola_id>', methods=['POST'])
@login_required
def elimina_scatola(scatola_id):
    scatola = Scatola.query.get_or_404(scatola_id)
    db.session.delete(scatola)
    db.session.commit()
    flash('Caja eliminada con éxito.')
    return redirect(url_for('home'))

# Rotta per visualizzare le scatole di un lotto specifico
@app.route('/lotto/<string:lotto>')
@login_required
def visualizza_lotto(lotto):
    scatole = Scatola.query.filter_by(lotto=lotto).order_by(Scatola.data.desc()).all()
    return render_template('lotto.html', lotto=lotto, scatole=scatole)

# Rotta per gestire i clienti
@app.route('/clienti', methods=['GET', 'POST'])
@login_required
def clienti():
    if request.method == 'POST':
        nome = request.form['nome']
        cliente = Cliente(nome=nome)
        db.session.add(cliente)
        db.session.commit()
        flash('Cliente agregado con éxito.')
        return redirect(url_for('clienti'))
    clienti = Cliente.query.order_by(Cliente.nome).all()
    return render_template('clienti.html', clienti=clienti)

# Rotta per eliminare un cliente
@app.route('/elimina_cliente/<int:cliente_id>', methods=['POST'])
@login_required
def elimina_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    # Controlla se il cliente ha vendite associate
    vendite_associate = Vendita.query.filter_by(cliente_id=cliente.id).first()
    if vendite_associate:
        flash('No es posible eliminar el cliente porque tiene ventas asociadas.')
        return redirect(url_for('clienti'))
    db.session.delete(cliente)
    db.session.commit()
    flash('Cliente eliminado con éxito.')
    return redirect(url_for('clienti'))

# Rotta per visualizzare le vendite
@app.route('/vendite')
@login_required
def vendite():
    vendite = Vendita.query.order_by(Vendita.data.desc()).all()
    return render_template('vendite.html', vendite=vendite)

# Rotta per inserire una nuova vendita
@app.route('/inserisci_vendita', methods=['GET', 'POST'])
@login_required
def inserisci_vendita():
    if request.method == 'POST':
        cliente_id = int(request.form['cliente_id'])
        data = datetime.strptime(request.form['data'], '%Y-%m-%d')
        tipo = request.form['tipo']
        peso = float(request.form['peso'])
        vendita = Vendita(
            cliente_id=cliente_id,
            data=data,
            tipo=tipo,
            peso=peso
        )
        db.session.add(vendita)
        db.session.commit()
        flash('Venta insertada con éxito.')
        return redirect(url_for('vendite'))
    clienti = Cliente.query.order_by(Cliente.nome).all()
    return render_template('inserisci_vendita.html', clienti=clienti)

# Rotta per eliminare una vendita
@app.route('/elimina_vendita/<int:vendita_id>', methods=['POST'])
@login_required
def elimina_vendita(vendita_id):
    vendita = Vendita.query.get_or_404(vendita_id)
    db.session.delete(vendita)
    db.session.commit()
    flash('Venta eliminada con éxito.')
    return redirect(url_for('vendite'))

# Rotta per la pagina Metriche (solo per Amministrazione)
@app.route('/metriche', methods=['GET'])
@login_required
def metriche():
    if current_user.ruolo != 'Amministrazione':
        flash('Acceso denegado: esta página está reservada para administradores.')
        return redirect(url_for('home'))

    # Inizializzazione delle variabili
    total_arrivati = None
    total_venduti = None

    # Gestione dei filtri per Trufas Llegadas
    data_inizio_arrivati = request.args.get('data_inizio_arrivati')
    data_fine_arrivati = request.args.get('data_fine_arrivati')

    if data_inizio_arrivati and data_fine_arrivati:
        data_inizio_arrivati = datetime.strptime(data_inizio_arrivati, '%Y-%m-%d')
        data_fine_arrivati = datetime.strptime(data_fine_arrivati, '%Y-%m-%d')

        scatole_filtrate = Scatola.query.filter(
            Scatola.data.between(data_inizio_arrivati, data_fine_arrivati)
        ).all()

        total_arrivati = sum(
            s.prima_scelta + s.seconda_scelta + s.trosos + s.scarti for s in scatole_filtrate
        )
    else:
        data_inizio_arrivati = data_fine_arrivati = None

    # Gestione dei filtri per Trufas Vendidas
    data_inizio_venduti = request.args.get('data_inizio_venduti')
    data_fine_venduti = request.args.get('data_fine_venduti')

    if data_inizio_venduti and data_fine_venduti:
        data_inizio_venduti = datetime.strptime(data_inizio_venduti, '%Y-%m-%d')
        data_fine_venduti = datetime.strptime(data_fine_venduti, '%Y-%m-%d')

        vendite_filtrate = Vendita.query.filter(
            Vendita.data.between(data_inizio_venduti, data_fine_venduti)
        ).all()

        total_venduti = sum(v.peso for v in vendite_filtrate)
    else:
        data_inizio_venduti = data_fine_venduti = None

    # Clienti Top senza filtro data
    clienti_ordinati = db.session.query(
        Cliente.nome,
        func.sum(Vendita.peso).label('totale_peso')
    ).join(Vendita).group_by(Cliente.id).order_by(desc('totale_peso')).all()

    return render_template(
        'metriche.html',
        total_arrivati=total_arrivati,
        total_venduti=total_venduti,
        clienti_ordinati=clienti_ordinati,
        data_inizio_arrivati=data_inizio_arrivati.strftime('%Y-%m-%d') if data_inizio_arrivati else '',
        data_fine_arrivati=data_fine_arrivati.strftime('%Y-%m-%d') if data_fine_arrivati else '',
        data_inizio_venduti=data_inizio_venduti.strftime('%Y-%m-%d') if data_inizio_venduti else '',
        data_fine_venduti=data_fine_venduti.strftime('%Y-%m-%d') if data_fine_venduti else ''
    )

# Caricamento dell'utente per Flask-Login
from app import login

@login.user_loader
def load_user(id):
    return Utente.query.get(int(id))
