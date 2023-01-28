from pymongo import MongoClient
from flask import Flask, render_template, request, session, jsonify
from datetime import datetime

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = ''
app.config['WTF_CSRF_ENABLED'] = True

client = MongoClient('')

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
        db_posts.insert_one(query)
      
    return render_template('index.html')


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    _posts = db_posts.find()

    return render_template('posts.html', posts=_posts)




@app.route('/api/posts', methods=['GET', 'POST'])
def api_posts():
    all_posts = list(db_posts.find())
    for post in all_posts:
        post['_id'] = str(post['_id'])

    return jsonify(all_posts)



if __name__ == '__main__':
    app.run(debug=True)
