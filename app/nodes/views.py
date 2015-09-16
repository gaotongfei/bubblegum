from flask import render_template, redirect, url_for, request
from . import bp
from .. import db
from .forms import CreateNodeForm
from ..models import Nodes, Post
from ..helpers import admin_required


@bp.route('/nodes', methods=['GET', 'POST'])
@admin_required
def nodes():
    form = CreateNodeForm()
    if form.validate_on_submit():
        try:
            node = Nodes(node=form.node.data)
            db.session.add(node)
            db.session.commit()
            return redirect(url_for('nodes.nodes'))
        except:
            db.session.rollback()
            return redirect(url_for('nodes.nodes'))
    nodes = Nodes.query.order_by(Nodes.create_time.desc()).all()
    return render_template('nodes/nodes.html', nodes=nodes, form=form)


@bp.route('/n/<node_name>', methods=['GET', 'POST'])
def topic_node(node_name):
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter_by(node=node_name).order_by(
        Post.post_time.desc()).paginate(page, per_page=15, error_out=False)
    posts = pagination.items
    nodes = Nodes.query.order_by(Nodes.create_time.desc()).all()
    return render_template('nodes/topic_node.html',
                           node_name=node_name,
                           pagination=pagination,
                           posts=posts,
                           nodes=nodes)
