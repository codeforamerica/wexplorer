from flask import Blueprint, current_app, redirect

blueprint = Blueprint('redirect', __name__)

@blueprint.route('/')
@blueprint.route('/<path>')
def redir(path=None):
    return redirect(current_app.config['REDIRECT_TO_HERE'])
