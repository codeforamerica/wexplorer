# -*- coding: utf-8 -*-

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)
from sqlalchemy import or_, distinct
from sqlalchemy.orm import load_only

from wexplorer.database import db
from wexplorer.explorer.models import (
    Company,
    CompanyContact,
    Contract,
    PurchasedItems
)
from wexplorer.explorer.util import SimplePagination

from wexplorer.explorer.forms import SearchBox, NewItemBox

blueprint = Blueprint('explorer', __name__, url_prefix='/explore',
                      static_folder="../static")

@blueprint.route('/', methods=['GET', 'POST'])
def search():
    '''
    The view for the basic search box.
    '''
    form = SearchBox(request.form)

    if request.args.get('q') is None:
        return render_template('explorer/explore.html', form=form)

    results = []
    search_for = request.args.get('q')
    page = int(request.args.get('page', 1))
    lower_bound = (page - 1) * 50
    upper_bound = lower_bound + 50

    companies = db.session.execute(
        '''
        SELECT a.company_id, b.contract_id, a.company, b.description
        FROM company a
        INNER JOIN contract b
        ON a.company_id = b.company_id
        LEFT OUTER JOIN company_purchases c
        ON a.company_id = c.company_id
        WHERE a.company ilike :search_for_wc
        OR b.description ilike :search_for_wc
        OR b.controller_number::VARCHAR = :search_for
        OR b.spec_number ilike :search_for_wc
        OR c.item ilike :search_for_wc
        ORDER BY a.company, b.description
        ''',
        {
            'search_for_wc': '%' + str(search_for)   + '%',
            'search_for': search_for,
        }
    ).fetchall()

    pagination = SimplePagination(page, 50, len(companies))

    for company in companies[lower_bound:upper_bound]:
        results.append({
            'company_id': company[0],
            'contract_id': company[1],
            'name': company[2],
            'description': company[3]
        })

    if len(results) == 0:
        results = None

    return render_template(
        'explorer/explore.html', form=form, names=results, pagination=pagination
    )

@blueprint.route('/companies/<company_id>', methods=['GET', 'POST'])
def companies(company_id, page=1):
    '''
    Simple profile page for companies
    '''
    iform = NewItemBox()
    page = int(request.args.get('page', 1))

    company = Company.query.filter(
        Company.company_id == company_id
    ).distinct().first()

    contacts = CompanyContact.query.distinct(
        CompanyContact.contact_name, CompanyContact.address_1,
        CompanyContact.address_2, CompanyContact.phone_number,
        CompanyContact.email,
    ).options(
        load_only(
            'contact_name', 'address_1', 'address_2', 'phone_number', 'email'
        )
    ).filter(CompanyContact.company_id == company_id).all()

    purchases = PurchasedItems.query.filter(
        PurchasedItems.company_id == company_id
    ).paginate(page, 5, False)

    return render_template(
        'explorer/companies.html',
        company=company,
        contacts=contacts,
        form=SearchBox(),
        iform=iform,
        purchases=purchases,
    )

@blueprint.route('/contracts/<contract_id>', methods=['GET'])
def contracts(contract_id):
    '''
    Simple profile page for individual contracts
    '''
    form = SearchBox(request.form)

    company = Company.query.join(Contract).filter(
        Contract.contract_id == contract_id
    ).first()

    return render_template(
        'explorer/contracts.html',
        company=company,
        form=form
    )

@blueprint.route('/companies/<company_id>/save', methods=['POST'])
def save_item(company_id):
    '''
    Redirect route for saving new purchased items
    '''
    form = NewItemBox(request.form)

    new_item = PurchasedItems(form.data.get('item'), company_id)
    db.session.add(new_item)
    db.session.commit()

    return redirect(url_for('explorer.companies', company_id=company_id))
