# -*- coding: utf-8 -*-
'''The app module, containing the app factory function.'''
from flask import Flask, render_template

from wexplorer.settings import ProdConfig, DevConfig
from wexplorer.assets import assets
from wexplorer.extensions import (
    bcrypt,
    cache,
    db,
    login_manager,
    migrate,
    debug_toolbar,
)
from wexplorer.utils import url_for_other_page
from wexplorer import shared, user, explorer
from wexplorer.redirect import blueprint as redirect_bp

def create_app(config_object=DevConfig):
    '''An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    '''
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    return app

def register_extensions(app):
    assets.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    app.jinja_env.globals['url_for_other_page'] = url_for_other_page
    return None

def register_blueprints(app):
    # app.register_blueprint(shared.views.blueprint)
    # app.register_blueprint(explorer.views.blueprint)
    app.register_blueprint(redirect_bp)
    return None

def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.html".format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None
