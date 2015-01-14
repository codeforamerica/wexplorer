# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from wexplorer.database import db
from wexplorer.explorer.models import (
    Company,
    CompanyContact,
    Contract
)

blueprint = Blueprint('explorer', __name__, url_prefix='/explore',
                      static_folder="../static")

@blueprint.route('/')
def explore_search():
    pass

@blueprint.route('/results')
def explore_results():

    companies = Company.query.all()
    names = []
    for company in companies:
        names.append({
            'name': company.company,
            'description': company.contracts.first().description
        })

    return render_template('explorer/explore.html', names=names)
