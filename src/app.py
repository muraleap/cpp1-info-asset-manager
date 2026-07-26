from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# データベース接続関数
def get_db_connection():
    conn = sqlite3.connect('book.db')
    conn.row_factory = sqlite3.Row
    return conn

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

# 追加画面
@app.route('/add-asset', methods=['GET', 'POST'])
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

        importance = request.form['importance']
        c = request.form['c']
        i = request.form['i']
        a = request.form['a']

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
    app.run(debug=True)

