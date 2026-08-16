from flask import Flask, render_template, request, redirect
import sqlite3
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.db'

app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        # Userのインスタンスを作成
        user = User(username=username, password=generate_password_hash(password, method='scrypt'))
        db.session.add(user)
        db.session.commit()
        return redirect('login')
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        # Userテーブルからusernameに一致するユーザを取得
        user = User.query.filter_by(username=username).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')
    else:
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('login')

# データベース接続関数
def get_db_connection():
    conn = sqlite3.connect('book.db')
    conn.row_factory = sqlite3.Row
    return conn

# 認証データベース接続関数
def get_auth_db_connection():
    auth_db_connection = sqlite3.connect('auth.db')
    auth_db_connection.row_factory = sqlite3.Row
    return auth_db_connection

# 初回リクエスト時にテーブルを作成
with app.app_context():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS book (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            name TEXT NOT NULL,
            note TEXT,
            user TEXT NOT NULL,
            bureau TEXT NOT NULL,
            charge TEXT NOT NULL,
            contact TEXT NOT NULL,
            media TEXT NOT NULL,
        
            importance INTEGER NOT NULL,
            c INTEGER NOT NULL,
            i INTEGER NOT NULL,
            a INTEGER NOT NULL,

            expire TEXT NOT NULL,
            registered TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    
    db.create_all()
    
# 追加画面
@app.route('/add-asset', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        #追加内容
        category = request.form['category']
        name = request.form['name']
        note = request.form['note']
        user = request.form['user']

        bureau = request.form['bureau']
        charge = request.form['charge']
        contact = request.form['contact']
        media = request.form['media']

        c = request.form['c']
        i = request.form['i']
        a = request.form['a']
        importance = max(c, i, a)

        expire = request.form['expire']
        registered = request.form['registered']

        conn = get_db_connection()
        # ? makes flask sanitising the query
        conn.execute('INSERT INTO book (category, name, note, user, bureau, charge, contact, media, importance, c, i, a, expire, registered) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (category, name, note, user, bureau, charge, contact, media, importance, c, i, a, expire, registered))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add_asset.html')

# 一覧表示
@app.route('/')
@login_required
def asset_list():
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM book').fetchall()
    conn.close()
    return render_template('assets_list.html', book=book)

# 削除機能
@app.route('/delete-asset/<int:id>', methods=['POST'])
def delete_asset(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM book WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000 ,debug=True)

