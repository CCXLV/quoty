from pymongo import MongoClient
from flask import Flask, render_template, request, session, jsonify, redirect, url_for
from datetime import datetime
from bson.objectid import ObjectId

from dotenv import load_dotenv

from utils.forbidden_words import FORBIDDEN_WORDS

load_dotenv('secrets.env')

SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("MONGODB_URL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = SECRET_KEY

client = MongoClient(DATABASE_URL)

db = client['ts']
db_posts = db['posts']


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        post_content = request.form.get('post-content')
        session['nickname'] = nickname
        session['post-content'] = post_content

        query = {
            'nickname': nickname,
            'content': post_content,
            'created_at': datetime.now()
        }
        error_message = 'It is highly forbidden using nsfw words!'
        found = False
        for word in FORBIDDEN_WORDS:
            if word in post_content or word in nickname:
                found = True
                break
        if found:
            return render_template('error.html', error=error_message)
        else:
            db_posts.insert_one(query)
        

    
    return render_template('index.html')


@app.route('/quotes', methods=['GET', 'POST'])
def posts():
    _posts = db_posts.find()

    return render_template('posts.html', posts=_posts)




@app.route('/api/quotes', methods=['GET', 'POST'])
def api_quotes():
    all_posts = list(db_posts.find())
    for post in all_posts:
        post['_id'] = str(post['_id'])

    return jsonify(all_posts)

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
    _posts = db_posts.find()

    return render_template('admin_room.html', posts=_posts)


@app.route('/quotes/delete', methods=['DELETE'])
def post_delete():
    _id = request.args.get('_id')
    try:
        db_posts.delete_one({"_id": ObjectId(_id)})
        return jsonify({"status": "success"})
    except:
        return jsonify({"status": "error"})



if __name__ == '__main__':
    app.run(debug=True)
