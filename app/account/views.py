from flask import (render_template, redirect, url_for, request, flash,
                   abort)
from flask.ext.login import (login_user, logout_user, login_required,
                             current_user)
from . import bp
from .. import db
from ..models import User, Post, Comment
from .forms import SignupForm, LoginForm, ProfileForm, AccountForm
from ..main.views import r


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('account.login'))
    return render_template('account/signup.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('main.index'))
    return render_template('account/login.html', form=form)


@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/settings/<type>', methods=['GET', 'POST'])
@login_required
def settings(type):
    username = current_user.username
    user = User.query.filter_by(username=username).first()
    form = ProfileForm()
    account_form = AccountForm()
    if type == 'profile':
        if form.validate_on_submit():
            user.website = form.website.data
            user.bio = form.bio.data
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        form.username.data = user.username
        form.website.data = user.website
        form.bio.data = user.bio
        return render_template('account/settings.html', form=form, type=type)
    if type == 'account':
        if account_form.validate_on_submit():
            if user.verify_password(account_form.current_password.data):
                user.password = account_form.new_password.data
                user.email = account_form.email.data
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('main.index'))
        account_form.email.data = user.email
        return render_template('account/settings.html',
                               account_form=account_form,
                               type=type)


@bp.route('/user/<username>', methods=['GET', 'POST'])
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    saved_topics = list(r.smembers('user-saved:'+str(user.id)))
    id_titles = []
    for i in saved_topics:
        id_title = {}
        id_title['id'] = i
        id_title['title'] = Post.query.filter_by(id=i).first().title
        id_titles.append(id_title)

    user_posts = Post.query.filter_by(username=username).\
        order_by(Post.post_time.desc()).limit(5).all()
    user_replies = Comment.query.filter_by(username=username).order_by(
        Comment.comment_time.desc()).limit(5).all()
    return render_template('account/user.html',
                           user=user,
                           user_posts=user_posts,
                           user_replies=user_replies,
                           id_titles=id_titles)
