from flask import render_template, request, redirect, url_for, session, flash, jsonify
from app import app
import sqlite3
import pandas as pd
from datetime import timedelta, date, datetime
from cryptography.fernet import Fernet
import random
import string
import qrcode
import os
import base64
import numpy as np
import cv2
from pyzbar.pyzbar import decode

app.config['SECRET_KEY'] = b'yD3EvddEQD5323GVHcuJcTAEDoH7Q-DzGmbr2aoSmh8='
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app/users.db'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(weeks=1)
app.config['UPLOAD_FOLDER'] = 'app/static/qrcode'

if not os.path.exists('app/static/qrcode'):
    os.mkdir(app.config['UPLOAD_FOLDER'])

columns_names = ['ID', 'Num_Unique', 'Qui', 'Enfant_Prénom', 'Enfant_Nom', 'Enfant_naissance', 'Prénom', 'Nom',
                 'Naissance', 'Telephone', 'Adresse', 'Association', 'Autres', 'Jour 1','Jour 2']

graph = None

jours = [date(2025,1,8),date(2025,3,6)]

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('app/formulaire.db')
    cur = conn.cursor()
    req = "SELECT * FROM participantes"
    cur.execute(req)
    data = cur.fetchall()
    conn.close()
    return render_template("index.html", columns=columns_names, data=data)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_logic',methods=['POST','GET'])
def login_logic():
    if request.method == 'POST':
        users = pd.read_sql('SELECT * FROM user', app.config['SQLALCHEMY_DATABASE_URI'])
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users['username'].values:
            cipher = Fernet(app.config['SECRET_KEY'])
            if cipher.decrypt(users[users['username'] == username]['password'].values[0].encode()) == password.encode():
                session['username'] = username
                return redirect(url_for('index'))
        flash('Invalid username or password','danger')
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('login'))
    
@app.route('/inscription_home')
def inscription_home():
    return render_template('inscription_home.html')

@app.route('/inscription')
def inscription():
    return render_template('form.html')

def generate_random_string(length=8):
    # Ensemble de caractères : lettres majuscules/minuscules et chiffres
    characters = string.ascii_letters + string.digits
    # Génération aléatoire
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

@app.route('/insertion',methods=['POST','GET'])
def insertData():
    if request.method == 'POST':
        correct = True
        data = {
            'who' : request.form.get('who', None),
            'child_firstname' : request.form.get('child-firstname', 'Null'),
            'child_lastname' : request.form.get('child-lastname','Null'),
            'child_birth' : request.form.get('child-birth','Null'),
            'firstname' : request.form.get('firstname',None),
            'lastname' : request.form.get('lastname',None),
            'birth' : request.form.get('birth',None),
            'numero' : request.form.get('numero',None),
            'association' : request.form.get('association',None),
            'autres': request.form.get('autres-asso',None),
            'address' : request.form.get('address',None),
        }
        conn = sqlite3.connect('app/formulaire.db')
        df = pd.read_sql('SELECT * FROM participantes', conn)
        if data['numero'] in df['numero'].values:
            if data['who'] == 'enfant':
                line = df[df['numero'] == data['numero']]
                if line['firstname'].values[0] != data['firstname'] and line['firstname'].values[0] != data['lastname'] or line['lastname'].values[0] != data['lastname'] and line['lastname'].values[0] != data['firstname']:
                    correct = False
                    erreur = 'Vos informations ne correspondent pas'
                elif line['association'].values[0] != data['association']:
                    correct = False
                    erreur = 'Un numéro de téléphone ne peut pas être associé à plusieurs associations'
                elif line['birth'].values[0] != data['birth']:
                    correct = False
                    erreur = 'Vos informations ne correspondent pas'
                else:
                    if line.shape[0] <= 3:
                        if data['birth'] in line['birth'].values:
                            child = df[df['birth'] == data['birth']]
                            if data['child_birth'] in child['child_birth'].values:
                                existing_child = child[child['child_birth'] == data['child_birth']]
                                if existing_child['child_firstname'].values[0] == data['child_firstname'] and existing_child['child_lastname'].values[0] == data['child_lastname']:
                                    correct = False
                                    erreur = 'Cet enfant est déjà inscrit'
                                else:
                                    values = data.values()
                                    columns = data.keys()
                                    values = list(data.values())
                                    columns = list(data.keys())
                                    unique = generate_random_string()
                                    while unique in df['num_unique'].values:
                                        unique = generate_random_string()
                                    columns.insert(1, 'num_unique')
                                    values.insert(1, unique)
                                    req = f"INSERT INTO participantes {tuple(columns)} VALUES {tuple(values)}"
                                    cur = conn.cursor()
                                    cur.execute(req)
                                    conn.commit()
                                    conn.close()
                                    qr_code = qrcode.make(unique)
                                    qr_code.save(f'app/static/qrcode/{unique}.png')
                                    qr_path = url_for('static',filename=f'qrcode/{unique}.png')
                                    if session.get('username',None) is not None:
                                        return redirect(url_for('index'))
                                    return render_template('success.html',qrcode_path=qr_path, name=data['child_firstname'],lastname=data['child_lastname'])
                            else:
                                values = data.values()
                                columns = data.keys()
                                values = list(data.values())
                                columns = list(data.keys())
                                unique = generate_random_string()
                                while unique in df['num_unique'].values:
                                    unique = generate_random_string()
                                columns.insert(1, 'num_unique')
                                values.insert(1, unique)
                                req = f"INSERT INTO participantes {tuple(columns)} VALUES {tuple(values)}"
                                cur = conn.cursor()
                                cur.execute(req)
                                conn.commit()
                                conn.close()
                                qr_code = qrcode.make(unique)
                                qr_code.save(f'app/static/qrcode/{unique}.png')
                                qr_path = url_for('static',filename=f'qrcode/{unique}.png')
                                if session.get('username',None) is not None:
                                    return redirect(url_for('index'))
                                return render_template('success.html', qrcode_path=qr_path, name=data['child_firstname'],lastname=data['child_lastname'])
                        else:
                            values = list(data.values())
                            columns = list(data.keys())
                            unique = generate_random_string()
                            while unique in df['num_unique'].values:
                                unique = generate_random_string()
                            columns.insert(1, 'num_unique')
                            values.insert(1, unique)
                            req = f"INSERT INTO participantes {tuple(columns)} VALUES {tuple(values)}"
                            cur = conn.cursor()
                            cur.execute(req)
                            conn.commit()
                            conn.close()
                            qr_code = qrcode.make(unique)
                            qr_code.save(f'app/static/qrcode/{unique}.png')
                            qr_path = url_for('static',filename=f'qrcode/{unique}.png')
                            if session.get('username',None) is not None:
                                return redirect(url_for('index'))
                            return render_template('success.html', qrcode_path=qr_path, name=data['child_firstname'],lastname=data['child_lastname'])
                    else:
                        correct = False
                        erreur = 'Vous avez atteint le nombre maximum d\'enfants inscrits'
                #df = df.append(data,ignore_index=True)
                #df.to_sql('participantes', conn, if_exists='replace', index=False)
            else:
                correct = False
                erreur = 'Vous êtes déjà inscrit(e). Si vous voulez inscrire un enfant veuillez selectionner \'Mon enfant\' au debut du formulaire !'
        else:
            values = data.values()
            columns = data.keys()
        if correct:
            values = list(data.values())
            columns = list(data.keys())
            unique = generate_random_string()
            while unique in df['num_unique'].values:
                unique = generate_random_string()
            columns.insert(1, 'num_unique')
            values.insert(1, unique)
            req = f"INSERT INTO participantes {tuple(columns)} VALUES {tuple(values)}"
            cur = conn.cursor()
            cur.execute(req)
            conn.commit()
            conn.close()
            qr_code = qrcode.make(unique)
            qr_code.save(f'app/static/qrcode/{unique}.png')
            qr_path = url_for('static',filename=f'qrcode/{unique}.png')
            if session.get('username',None) is not None:
                return redirect(url_for('index'))
            return render_template('success.html', qrcode_path=qr_path, name=data['firstname'],lastname=data['lastname'])
        else:
            return render_template('form.html',erreur=erreur)

@app.route('/recovery')
def recovery():
    erreur = session.get('error',None)
    return render_template('recovery.html',erreur=erreur)

@app.route('/recovering',methods=['POST'])
def recovering():
    session['error'] = None
    if request.method == 'POST':
        who = request.form.get('who', None)
        child_firstname = request.form.get('child-firstname',None)
        child_birth = request.form.get('child-birth',None)
        birth = request.form.get('birth',None)
        numero = request.form.get('numero',None)
        association = request.form.get('association',None)
        conn = sqlite3.connect('app/formulaire.db')
        df = pd.read_sql('SELECT * FROM participantes', conn)
        if numero in df['numero'].values:
            lines = df[df['numero'] == numero]
            if birth == lines['birth'].values[0] and association == lines['association'].values[0]:
                if who == 'enfant':
                    children = lines[lines['child_birth'] == child_birth]
                    child = children[children['child_firstname'] == child_firstname]
                    unique = child['num_unique'].values[1]
                    qr_url = url_for('static',filename=f'qrcode/{unique}.png')
                    session['error'] = None
                    return render_template('recovery_found.html',qr_url=qr_url, firstname=child['child_firstname'].values[1], lastname=child['child_lastname'].values[1], association=child['association'].values[1], who=who, parent_firstname=child['firstname'].values[1], parent_lastname=child['lastname'].values[1])
                else:
                    unique = lines['num_unique'].values[0]
                    qr_url = url_for('static',filename=f'qrcode/{unique}.png')
                    session['error'] = None
                    return render_template('recovery_found.html', qr_url=qr_url, firstname=lines['firstname'].values[0], lastname=lines['lastname'].values[0], association=lines['association'].values[0])
            else:
                session['error'] = 'Vos informations ne sont pas correctes ou non enrégistrées'
                return redirect(url_for('recovery'))
        else:
            session['error'] = 'Vos informations ne sont pas correctes ou non enrégistrées'
            return redirect(url_for('recovery'))

@app.route('/scanner',methods=['POST','GET'])
def scanner():
    return render_template('qr_scanner.html')

@app.route('/scan_process', methods=['POST','GET'])
def scan_process():
    if request.method == 'GET':
        return redirect(url_for('scanner'))
    image_data = request.form.get('image')
    if image_data:
        # Décoder l'image base64
        header, encoded = image_data.split(",", 1)
        image_bytes = base64.b64decode(encoded)
        np_arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Décoder les QR codes
        decoded_objects = decode(img)
        if decoded_objects:
            result = [obj.data.decode("utf-8") for obj in decoded_objects]
        return redirect(url_for('scan_qr',unique=result[0]))
    else:
        return render_template('qr_scanner.html', erreur="Aucun QR code detecté ! Veuillez réessayer en exposant bien le QR à la caméra. Si la caméra ne s'affiche pas, rafraîchissez la page")
    
@app.route('/result/<unique>')
def scan_qr(unique):
    conn = sqlite3.connect('app/formulaire.db')
    cur = conn.cursor()
    req = f"SELECT * FROM participantes WHERE num_unique='{unique}'"
    cur.execute(req)
    data = cur.fetchall()
    conn.close()
    if len(data) > 0:
        if date.today() == jours[0]:
            status = data[0][12]
        elif date.today() == jours[1]:
            status = data[0][13]
        else:
            status = "En attente"
    
        if data[0][2] == 'enfant':
            today = date.today()
            return render_template('found.html', firstname=data[0][3], lastname=data[0][4],birth=data[0][5], association=data[0][-1], num_unique=data[0][1], date_jour=str(today), status=status)
        else:
            today = date.today()
            return render_template('found.html', firstname=data[0][6], lastname=data[0][7],birth=data[0][8], association=data[0][-1], num_unique=data[0][1], date_jour=str(today), status=status)
    else:
        return render_template('qr_scanner.html', erreur="QR code non réconnu !")

@app.route("/presence/<unique>")
def presence(unique):
    conn = sqlite3.connect("app/formulaire.db")
    cur = conn.cursor()
    if date.today() == jours[0]:
        req = "UPDATE participantes SET jour1=? WHERE num_unique= ?"
        cur.execute(req, ('presente',unique))
        conn.commit()
    elif date.today() == jours[1]:
        req = "UPDATE participantes SET jour2=? WHERE num_unique= ?"
        cur.execute(req, ('presente',unique))
        conn.commit()
    conn.close()
    return redirect(url_for('scan_qr',unique=unique))

@app.route('/malidev')
def malidev():
    return redirect('https://www.malideveloppeur.com')