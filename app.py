import os
import sqlite3
from flask import Flask, request, render_template, redirect, session, flash, url_for
from models import db, User, Post, Comment
app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'

@app.route('/', methods=['GET','POST'])
def home():
    if 'username' not in session:
        flash('로그인하십시오', '')
        return redirect('/login/')

    if request.method == 'POST':
        username = request.form.get('inputText')
    else:
        username = session['username'] 

    flash('hello, {}'.format(username))
    return render_template("home.html")

@app.route('/post_list/', methods=['GET', 'POST'])
def post_list():
    post_list = Post.query.order_by(Post.datetime.asc())
    return render_template("post_list.html", post_list=post_list)

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		f = request.files['file']
		f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
		return 'Upload Success'

	else:
		return """
		<form action="/fileUpload" method="POST" enctype="multipart/form-data">
			<input type="file" name="file" />
			<input type="submit"/>
		</form>
		"""

@app.route('/post/', methods=['GET','POST'])
def post():
    if request.method == "GET":
        return render_template('post.html')

    title = request.form.get('title')
    content = request.form.get('content')

    if not(title and content):
        return "입력되지 않은 정보가 있습니다"

    posttable = Post()
    posttable.title = title
    posttable.content = content
    posttable.username = session['username']  # post가 작성자 username에 대한 정보를 포함하도록 변경

    db.session.add(posttable)
    db.session.commit()
    return redirect('/post_list')

@app.route('/detail/<int:post_id>/')
def detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post_detail.html", post=post)

@app.route('/delete/<int:post_id>/')
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.username == session['username']:  # post의 작성자와 로그인된 사용자가 같을때만 delete 실행
        db.session.delete(post)
        db.session.commit()
        return redirect('/post_list/')
    else:
        return "게시글은 작성자만 삭제할 수 있습니다"

@app.route('/detail/<int:post_id>/comment/', methods=['GET', 'POST'])
def comment(post_id):
    if request.method == 'GET':
        return render_template("comment.html")

    content = request.form.get('content')

    post = Post.query.get_or_404(post_id)
    comment = Comment()
    comment.content = content
    comment.post = post
    comment.post_id = post_id

    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('detail', post_id=post_id))
    
@app.route('/signup/', methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")

    username = request.form.get('username')
    password = request.form.get('password')

    if not(username):
        return "사용자 이름이 입력되지 않았습니다"

    usertable=User()
    usertable.username = username
    usertable.password = password

    db.session.add(usertable)
    db.session.commit()
    return redirect('/')
    
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form.get('username')
    password = request.form.get('password')

    # print(username) -> 터미널창에서 username 확인 가능, 디버깅 시 사용

    if not(username and password):
        return "입력되지 않은 정보가 있습니다"
    else: # login 부분에서 비밀번호가 틀려도 로그인되고, [username, password]를 반환하던 점 수정
        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                session['username'] = username
                return redirect('/')
            else:
                return "비밀번호가 다릅니다"
        else:
            return "사용자가 존재하지 않습니다"

@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == "__main__":
    with app.app_context():
        basedir = os.path.abspath(os.path.dirname(__file__)) # 현재 파일이 있는 폴더 경로
        dbfile = os.path.join(basedir, 'db.sqlite') # 데이터베이스 파일 생성

        app.config['SECRET_KEY'] = "ICEWALL" # 세션관리 및 암호화를 위한 시크릿키 설정
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
        app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        db.init_app(app)
        # db.app = app
        db.create_all()

        try:
            ip = os.environ["ICEWALL"]
        except KeyError:
            ip = "127.0.0.1"

        app.run(host=ip, port=5001, debug=True)
