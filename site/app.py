from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '11111'
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/blog', methods=['POST', 'GET'])
# Обработка получения из формы и сохранения записи в базе
def blog():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']

        article = Article(title=title, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            flash('Сообщение отправлено', category='success')
            return redirect('/blog')

        except Exception:
            logging.exception('')
            return ''

    else:
        articles = Article.query.all()
        return render_template("blog.html", articles=articles)


@app.route('/blog/<int:id>')
# Обработка отображения записи
def blog_record(id):
    article = Article.query.get(id)
    return render_template("blog_record.html", article=article)

@app.route('/blog/<int:id>/delete')
# Обработка удаления записи
def record_delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        flash('Сообщение удалено', category='delete')
        return redirect('/blog')
    except:
        return "При удалении записи произошла ошибка"

@app.route('/blog/<int:id>/update', methods=['POST', 'GET'])
def record_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/blog')

        except Exception:
            logging.exception('')
            return ''

    else:
        return render_template("record_update.html", article=article)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)


