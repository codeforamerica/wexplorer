# -*- coding: utf-8 -*-
'''Public section, including homepage and signup.'''
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)

from wexplorer.database import db

blueprint = Blueprint('public', __name__, static_folder="../static")

@blueprint.route("/", methods=["GET", "POST"])
def home():
    return redirect(url_for('explorer.explore_search'))

@blueprint.route("/about")
def about():
    return render_template("public/about.html")
