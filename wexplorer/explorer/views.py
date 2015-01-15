# -*- coding: utf-8 -*-
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)
from sqlalchemy import or_

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
    # if request.method == 'POST':
    if request.args.get('q') is None:
        return render_template('explorer/explore.html', form=form)

    results = []
    search_for = request.args.get('q')

    companies = Company.query.join(Contract).filter(or_(
        Company.company.like('%' + search_for + '%'),
        Contract.description.ilike('%' + search_for + '%')
    )).all()

    for company in companies:
        results.append({
            'name': company.company,
            'description': company.contracts.first().description
    })

    if len(results) == 0:
        results = None

    return render_template(
        'explorer/explore.html', form=form, names=results, term=search_for
    )

