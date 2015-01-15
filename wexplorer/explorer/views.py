# -*- coding: utf-8 -*-
from flask import (
    Blueprint,
    render_template,
    request
)

from wexplorer.database import db
from wexplorer.explorer.models import (
    Company,
    CompanyContact,
    Contract
)

from wexplorer.explorer.forms import SearchBox

blueprint = Blueprint('explorer', __name__, url_prefix='/explore',
                      static_folder="../static")

@blueprint.route('/', methods=['GET', 'POST'])
def explore_search():
    form = SearchBox(request.form)
    if request.method == 'POST':
        pass
    return render_template('explorer/explore_search.html', form=form)

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
