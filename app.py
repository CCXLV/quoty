from cs50 import SQL
from flask import Flask, jsonify, redirect, render_template, request
from datetime import datetime

from utils.forbidden_words import FORBIDDEN_WORDS
import config

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = config.SECRET_KEY

db = SQL(config.MySQL_URL)


CATEGORIES = [
    'Motivational', 
    'Inspirational',
    'Wise',
    'Movie',
    'Other'
]
categories = [
    'Motivational', 
    'Inspirational',
    'Wise',
    'Movie'
]


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        author = request.form.get('author')
        post_content = request.form.get('post-content')
        category = request.form.get('category')

        error_message = 'It is highly forbidden using nsfw words!'
        found = False
        if category not in CATEGORIES:
            return render_template('error.html', error='Choose correct category.')

        for word in FORBIDDEN_WORDS:
            if word in post_content or word in author:
                found = True
                break
        if found:
            return render_template('error.html', error=error_message)
        else:
            query_ = (
                'INSERT INTO posts (author, content, upload_date, category) VALUES (?, ?, ?, ?)'
            )
            db.execute(query_, author, post_content, datetime.now(), category)
    
    return render_template('index.html', categories=categories)


@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/api/quotes', methods=['GET', 'POST'])
def api_quotes():
    result = db.execute('SELECT * FROM posts')


    return jsonify(result)

@app.route('/quotes', methods=['GET', 'POST'])
def posts():
    result = db.execute('SELECT * FROM posts')
    results = []
    for i in result:
        results.append(i)

    return render_template('posts.html', posts=results)

@app.route('/quotes/<category>')
def postss(category):
    results = db.execute('SELECT * FROM posts WHERE category = ?', str(category))

    return render_template('posts.html', posts=results)


@app.route('/admin', methods=['GET', 'POST'])
def admin():

    return render_template('admin.html')


@app.route('/admin/verify-passcode', methods=['POST'])
def verify_passcode():
    message = 'Acces denied!'
    passcode = request.form.get('passcode')
    if passcode == config.ADMIN_PASSWORD:
        return redirect('/admin/room')
    else:
        return render_template('error.html', error=message)


@app.route('/admin/room/IC12S8AfOfPLmaX8rSso7pL6', methods=['GET', 'POST'])
def admin_room():
    result = db.execute('SELECT * FROM posts')
    results = []
    for i in result:
        results.append(i)

    return render_template('admin_room.html', posts=results)


@app.route('/quotes/delete', methods=['DELETE'])
def post_delete():
    id = request.args.get('_id')
    try:
        db.execute('DELETE FROM posts WHERE id = ?', id)
        return jsonify({"status": "success"})
    except:
        return jsonify({"status": "error"})



if __name__ == '__main__':
    app.run(debug=True)
