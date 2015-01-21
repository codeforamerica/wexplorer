# -*- coding: utf-8 -*-
'''Public section, including homepage and signup.'''
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)

from wexplorer.database import db
from wexplorer.explorer.forms import SearchBox

blueprint = Blueprint('shared', __name__, static_folder="../static")

@blueprint.route("/", methods=["GET", "POST"])
def home():
    return redirect(url_for('explorer.search'))

@blueprint.route("/about")
def about():
    form = SearchBox()
    return render_template("shared/about.html", form=form)
