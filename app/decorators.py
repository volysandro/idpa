from functools import wraps
from flask_login import current_user
from flask import flash, abort, redirect, url_for

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not current_user.admin:
            return redirect(url_for('main.profile'))

        return f(*args, **kwargs)

    return decorated_function