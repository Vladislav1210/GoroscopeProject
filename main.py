import sqlalchemy
import parser
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, redirect, render_template, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from data import db_session
from data.db_session import SqlAlchemyBase

from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String)
    password = sqlalchemy.Column(sqlalchemy.String)

    def check_password(self, password2):
        return check_password_hash(self.password, password2)


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Придумайте пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/main")

        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, title='Авторизация')

    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
def start():
    return render_template('start.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = User()
        user.email = form.email.data
        user.password = generate_password_hash(form.password.data)

        db_sess.add(user)
        db_sess.commit()
        db_sess.close()
        return redirect('/main')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/main', methods=['POST', 'GET'])
def main():
    text = ''
    if request.method == 'GET':
        return render_template('main.html', text=text)
    elif request.method == 'POST':
        frm = request.form['znak']
        text = f'{frm} - ' + parser.parser(frm)
        return render_template('main.html', text=text)


if __name__ == '__main__':
    db_session.global_init("db/blogs.sqlite")
    app.run(port=8080, host='127.0.0.2')
