from cs50 import SQL
from flask import Flask, render_template, redirect, request, url_for, session


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = ''

db =  SQL("")


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        post_content = request.form.get('post-content')
        session['nickname'] = nickname
        session['post-content'] = post_content

        db.execute('INSERT INTO posts (nickname, content) VALUES (?, ?)', nickname, post_content)



    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
