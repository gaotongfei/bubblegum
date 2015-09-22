from flask import render_template
from ..helpers import admin_required
from . import bp


@bp.route('/admin', methods=['GET', 'POST'])
@admin_required
def admin():
    return "hello admin"
