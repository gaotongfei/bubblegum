from flask import (render_template, redirect, url_for,
                   abort, request, jsonify, flash, g)
from .forms import PostTopicForm, CommentForm
from . import bp
from .. import db
from flask.ext.login import current_user, login_required
from ..models import Post, Comment, Notification, User, Nodes
from ..helpers import gravatar_url, admin_required
import mistune
from ..filters import mention, mention_username, bleach_html
from datetime import datetime
import warnings
from sqlalchemy import exc as sa_exc
import redis


markdown = mistune.Markdown()
pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)
warnings.simplefilter("ignore", category=sa_exc.SAWarning)


@bp.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.latest_update_time.desc()).paginate(page, per_page=15, error_out=False)
    posts = pagination.items
    user_num = User.query.count()
    topic_num = Post.query.count()
    comment_num = Comment.query.count()
    nodes = Nodes.query.order_by(Nodes.create_time.desc()).all()
    if current_user.is_authenticated():
        message_count = Notification.query.filter_by(to_id=current_user.username).filter_by(is_read=0).count()
        return render_template(
            'main/index.html',
            posts=posts,
            message_count=message_count,
            pagination=pagination,
            user_num=user_num,
            topic_num=topic_num,
            comment_num=comment_num,
            nodes=nodes
        )
    else:
        return render_template(
            'main/index.html',
            posts=posts,
            pagination=pagination,
            user_num=user_num,
            topic_num=topic_num,
            comment_num=comment_num,
            nodes=nodes
        )


@bp.route('/post-topic', methods=['GET', 'POST'])
@login_required
def post_topic():
    form = PostTopicForm()
    if form.validate_on_submit():
        avatar_url = gravatar_url(current_user.email, 40)
        if Nodes.query.filter_by(node=form.node.data).first() is not None:
            post = Post(
                user_id=current_user.id,
                title=form.title.data,
                body=form.body.data,
                body_md=bleach_html(markdown(form.body.data)),
                node=form.node.data,
                username=current_user.username,
                avatar=avatar_url
            )
            db.session.add(post)
            db.session.commit()
        else:
            flash('node doesn\'t exists')
        return redirect(url_for('main.index'))
    return render_template(
        'main/post-topic.html',
        form=form
    )


@bp.route('/topic/<int:id>', methods=['GET', 'POST'])
def topic(id):
    form = CommentForm()
    if form.validate_on_submit():
        avatar_url = gravatar_url(current_user.email, 40)
        comment = Comment(
            topic_id=id,
            comment=bleach_html(markdown(mention(form.comment.data))),
            username=current_user.username,
            avatar=avatar_url)
        post = Post.query.filter_by(id=id).first()
        post.latest_update_time = datetime.utcnow()
        username_ids = mention_username(form.comment.data)
        if len(username_ids) > 0:
            for username_id in username_ids:
                user_query = User.query.filter_by(username=username_id).first()
                if user_query is not None:
                    to_id = user_query.username
                    notification = Notification(
                        to_id=to_id,
                        from_post_id=id,
                        from_post_title=Post.query.filter_by(id=id).first().title,
                        from_id=current_user.username,
                        message=bleach_html(markdown(form.comment.data))
                    )
                    db.session.add(notification)
                    db.session.commit()
        db.session.add(comment)
        db.session.commit()
        return redirect('/topic/' + str(id))

    topic = Post.query.get_or_404(id)
    comments = Comment.query.filter_by(topic_id=id).order_by(Comment.comment_time).all()
    message_count = None

    saved = False

    if current_user.is_authenticated():
        message_count = Notification.query.filter_by(to_id=current_user.username).\
            filter_by(is_read=0).count()
        saved_topics = list(r.smembers('user-saved:' + str(current_user.id)))
        if str(id) in saved_topics:
            saved = True

    r.incr('click-count:' + str(id))
    click_count = r.get('click-count:' + str(id))

    return render_template(
        'main/topic.html',
        topic=topic,
        form=form,
        comments=comments,
        message_count=message_count,
        click_count=click_count,
        saved=saved
    )


@bp.route('/delete/<int:id>', methods=['GET', 'POST'])
@admin_required
def delete(id):
    posts = Post.query.get_or_404(id)
    comments = Comment.query.filter_by(topic_id=id).all()
    notifications = Notification.query.filter_by(from_post_id=id).all()
    db.session.delete(posts)

    for comment in comments:
        db.session.delete(comment)

    for notification in notifications:
        db.session.delete(notification)

    r.srem('user-saved:' + str(posts.user_id), id)

    db.session.commit()
    return redirect(url_for('main.index'))


@bp.route('/message/<username>', methods=['GET', 'POST'])
@login_required
def message(username):
    if current_user.is_authenticated():
        if current_user.username != username:
            abort(403)
        else:
            notifications = Notification.query.filter_by(to_id=username).\
                            order_by(Notification.message_time.desc()).all()
            return render_template('main/message.html', notifications=notifications)
    return render_template('main/message.html')


@bp.route('/message_is_read', methods=['GET', 'POST'])
def message_is_read():
    is_read = request.args.get('is_read', type=int)
    message_id = request.args.get('message_id', type=int)
    if message_id is not None:
        notification = Notification.query.filter_by(id=message_id).first()
        notification.is_read = 1
        db.session.commit()
    return jsonify(
        is_read=is_read,
        message_id=message_id
    )


@bp.route('/search', methods=['POST'])
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('main.index'))
    return redirect(
        url_for(
            'main.search_results',
            query=g.search_form.search.data
        )
    )


@bp.route('/search_results/<query>')
def search_results(query):
    results = Post.query.whoosh_search(query, 10, or_=True).all()
    return render_template(
        'main/search_results.html',
        query=query,
        results=results
    )


@bp.route('/save/<id>', methods=['GET', 'POST'])
@login_required
def save(id):
    r.sadd('user-saved:' + str(current_user.id), id)
    return redirect(request.args.get('next') or request.referrer)


@bp.route('/unsave/<id>', methods=['GET', 'POST'])
@login_required
def unsave(id):
    r.srem('user-saved:' + str(current_user.id), id)
    return redirect(request.args.get('netx') or request.referrer)
