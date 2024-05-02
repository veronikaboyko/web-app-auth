from flask import Flask, request, render_template, redirect, session, url_for
import firebase_admin
from firebase_admin import credentials, db
from vk_authorization import get_authorization_url, get_access_token, get_user_data

app = Flask(__name__)
app.secret_key = '%1^1$Av*r!$*cR*^k*(!)'

cred = credentials.Certificate('credentials.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://notes-web-app-47212-default-rtdb.europe-west1.firebasedatabase.app'})

ref = db.reference('/')


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    if session.get('auth') is not None:
        return render_template('main.html')
    else:
        return render_template('index.html')


@app.route('/sign_in', methods=['GET'])
def sign_in():
    authorization_url = get_authorization_url()
    return redirect(authorization_url)


@app.route('/callback', methods=['GET'])
def callback():
    code = request.args.get('code')
    if code:
        access_token, user_id = get_access_token(code)
        session['user_id'] = user_id
        session['access_token'] = access_token
        user_data = get_user_data(access_token, user_id)
        session['first_name'] = user_data[0]['first_name']
        session['last_name'] = user_data[0]['last_name']
        session['auth'] = True
        return redirect(url_for('main'))
    else:
        return redirect(url_for('index'))


@app.route('/sign_out', methods=['GET'])
def sign_out():
    if session.get('auth') is not None:
        session.pop('user_id')
        session.pop('first_name')
        session.pop('last_name')
        session.pop('auth')

    return redirect(url_for('index'))


@app.route('/main', methods=['GET'])
def main():
    if session.get('auth') is not None:
        first_name = session.get('first_name')
        last_name = session.get('last_name')
        user_id = session.get('user_id')
        notes = ref.child(f'{user_id}').get()
        if notes is not None:
            n = notes
        else:
            n = {}
        return render_template('main.html', name=f'{first_name} {last_name}', notes=n)
    else:
        return redirect(url_for('index'))


@app.route('/add_note', methods=['POST'])
def add_note():
    note = request.form['note']
    user_id = session.get('user_id')
    ref.child(f'{user_id}').push(note)
    return redirect(url_for('main'))


@app.route('/delete_note', methods=['POST'])
def delete_note():
    user_id = session.get('user_id')
    note_to_delete = request.form['note_id']
    ref.child(f'{user_id}').child(note_to_delete).delete()
    return redirect(url_for('main'))
