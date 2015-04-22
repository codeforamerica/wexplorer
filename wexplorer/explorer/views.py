# -*- coding: utf-8 -*-
import datetime
import time
import re
import os
from werkzeug import secure_filename
from flask import (
    Blueprint, render_template, request,
    current_app, jsonify
)
from sqlalchemy.orm import load_only

from wexplorer.database import db
from wexplorer.explorer.models import (
    Company, CompanyContact, Contract, LastUpdated
)
from wexplorer.explorer.util import SimplePagination
from wexplorer.explorer.forms import SearchBox, NewItemBox, FileUpload
from wexplorer.data_update import update

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
        WHERE a.company ilike :search_for_wc
        OR b.description ilike :search_for_wc
        OR b.controller_number::VARCHAR = :search_for
        OR b.contract_number ilike :search_for_wc
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

    updated = LastUpdated.query.first()
    if updated:
        last_updated = datetime.datetime.strftime(
            LastUpdated.query.first().last_updated, '%b %d %Y'
        )
    else:
        last_updated = None

    return render_template(
        'explorer/explore.html', form=form, names=results, pagination=pagination, last_updated=last_updated
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

    return render_template(
        'explorer/companies.html',
        company=company,
        contacts=contacts,
        form=SearchBox(),
        iform=iform
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

    contract = company.contracts[0]
    contract_href = None
    if contract.contract_number and contract.type_of_contract.lower() == 'county':
        # first try to convert it to an int
        try:
            _contract_number = int(float(contract.contract_number))
            contract.contract_number = _contract_number
        # if you can't, it has * or other characters, so just
        # strip down to the digits
        except ValueError:
            if '**' in contract.contract_number:
                _contract_number = int(re.sub(r'i?\D', '', contract.contract_number))
            elif '*' in contract.contract_number:
                _contract_number = None
            elif 'i' in contract.contract_number:
                _contract_number = contract.contract_number


        # take the result and stick it into the well-formed county urls
        contract_href = 'http://apps.county.allegheny.pa.us/BidsSearch/pdf/{number}.pdf'.format(
            number=_contract_number
        ) if _contract_number else None

    return render_template(
        'explorer/contracts.html',
        company=company,
        contract=contract,
        form=form,
        contract_href=contract_href
    )

@blueprint.route('/upload_new', methods=['GET', 'POST'])
def upload():
    form = FileUpload()
    if form.validate_on_submit():
        _file = request.files.get('upload')
        filename = secure_filename(_file.filename)
        filepath = os.path.join(current_app.config.get('UPLOAD_FOLDER'), filename)
        _file.save(filepath)
        return render_template('explorer/upload_success.html', filepath=filepath)
    else:
        return render_template('explorer/upload_new.html', form=form)

@blueprint.route('/_process_file', methods=['POST'])
def process_upload():
    filepath = request.form.get('filepath')
    result = update(filepath)
    if result.get('status') == 'success':
        last_updated = LastUpdated.query.first()
        if not last_updated:
            last_updated = LastUpdated(datetime.datetime.utcnow())
            db.session.add(last_updated)
        else:
            last_updated.last_updated = datetime.datetime.utcnow()
        db.session.commit()
        return jsonify(result), 200
    else:
        return jsonify(result), 403

@blueprint.route('/_status')
def check_status():
    response = {}
    response['status'] = 'ok'
    try:
        Contract.query.first()
    except:
        response['status'] = 'Database is unavailable'
    response['updated'] = int(time.time())
    response['dependencies'] = []
    return jsonify(response)
