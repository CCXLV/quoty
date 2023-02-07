from cs50 import SQL
from flask import Flask, render_template, request, session, jsonify, redirect, url_for
from datetime import datetime

from dotenv import load_dotenv

from utils.forbidden_words import FORBIDDEN_WORDS

load_dotenv('secrets.env')

SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("MySQL_URL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = SECRET_KEY

db = SQL(DATABASE_URL)



@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        post_content = request.form.get('post-content')
        session['nickname'] = nickname
        session['post-content'] = post_content

        error_message = 'It is highly forbidden using nsfw words!'
        found = False
        for word in FORBIDDEN_WORDS:
            if word in post_content or word in nickname:
                found = True
                break
        if found:
            return render_template('error.html', error=error_message)
        else:
            query_ = (
                'INSERT INTO posts (author, content, upload_date) VALUES (?, ?, ?)'
            )
            db.execute(query_, author, post_content, datetime.now())
        

    
    return render_template('index.html')


@app.route('/quotes', methods=['GET', 'POST'])
def posts():
    result = db.execute('SELECT * FROM posts')
    results = []
    for i in result:
        results.append(i)

    return render_template('posts.html', posts=results)


@app.route('/api/quotes', methods=['GET', 'POST'])
def api_quotes():
    result = db.execute('SELECT * FROM posts')

    return jsonify(result)

@app.route('/admin', methods=['GET', 'POST'])
def admin():

    return render_template('admin.html')


@app.route('/admin/verify-passcode', methods=['POST'])
def verify_passcode():
    message = 'Acces denied!'
    passcode = request.form.get('passcode')
    if passcode == ADMIN_PASSWORD:
        return redirect('/admin/room/IC12S8AfOfPLmaX8rSso7pL6')
    else:
        return render_template('error.html', error=message)

@app.route('/admin/room/IC12S8AfOfPLmaX8rSso7pL6', methods=['POST'])
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
