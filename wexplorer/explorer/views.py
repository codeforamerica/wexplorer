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
    Contract,
    PurchasedItems
)

from wexplorer.explorer.forms import SearchBox, NewItemBox

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
            'company_id': company.company_id,
            'contract_id': company.contracts[0].contracts_id,
            'name': company.company,
            'description': company.contracts[0].description
    })

    if len(results) == 0:
        results = None

    return render_template(
        'explorer/explore.html', form=form, names=results, term=search_for
    )

@blueprint.route('/companies/<int:company_id>/save', methods=['POST'])
def save_item(company_id):
    form = NewItemBox(request.form)

    new_item = PurchasedItems(form.data.get('item'), company_id)
    db.session.add(new_item)
    db.session.commit()

    return redirect(url_for('explorer.explore_companies', company_id=company_id))



@blueprint.route('/companies/<int:company_id>', methods=['GET', 'POST'])
def explore_companies(company_id):
    form = NewItemBox(request.form)

    company = Company.query.join(CompanyContact).filter(
        Company.company_id == company_id
    ).first()

    return render_template(
        'explorer/companies.html', company=company, form=form
    )

@blueprint.route('/contracts/<int:contract_id>', methods=['GET'])
def explore_contracts(contract_id):

    company = Company.query.join(Contract).filter(
        Contract.contracts_id == contract_id
    ).first()

    return render_template(
        'explorer/contracts.html', company=company
    )
