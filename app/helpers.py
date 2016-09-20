from datetime import datetime
from functools import wraps
from hashlib import md5
from flask_login import current_user
from flask import abort


def time_delta(post_time):
    now = datetime.utcnow()
    delta = (now - post_time).total_seconds()
    if delta < 60:
        return "just now"
    elif delta < 3600:
        return "%d minutes ago" % (delta // 60) if (delta // 60) > 1 else "%d minute ago" % (delta // 60)
    elif delta < 86400:
        return "%d hours ago" % (delta // 3600) if (delta // 3600) > 1 else "%d hour ago" % (delta // 3600)
    else:
        return "%d days ago" % (delta // 86400) if (delta // 86400) > 1 else "%d day ago" % (delta // 86400)
    return delta


def gravatar_url(email, size):
    return 'https://gravatar.com/avatar/%s?d=retro&s=%d' % (md5(email.encode('utf-8')).hexdigest(), size)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.id != 1:
                abort(403)
            return f(*args, **kwargs)
        else:
            abort(403)
    return decorated_function
