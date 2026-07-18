from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# データベース接続関数
def get_db_connection():
    conn = sqlite3.connect('books.db')
    conn.row_factory = sqlite3.Row
    return conn

# 初回リクエスト時にテーブルを作成
with app.app_context():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 本の追加画面
@app.route('/add-book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        conn = get_db_connection()
        conn.execute('INSERT INTO books (title, author) VALUES (?, ?)', (title, author))
        conn.commit()
        conn.close()
        return redirect('/books')
    return render_template('add_book.html')

# 本の一覧表示
@app.route('/books')
def book_list():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return render_template('book_list.html', books=books)

# 本の削除機能
@app.route('/delete-book/<int:id>', methods=['POST'])
def delete_book(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM books WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/books')

if __name__ == '__main__':
    app.run(debug=True)

