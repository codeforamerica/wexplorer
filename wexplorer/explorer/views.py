# -*- coding: utf-8 -*-
import os
from werkzeug import secure_filename
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, current_app, jsonify
)
from flask.ext.uploads import UploadSet
from sqlalchemy import or_, distinct
from sqlalchemy.orm import load_only

from wexplorer.database import db
from wexplorer.explorer.models import (
    Company,
    CompanyContact,
    Contract
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

    import pdb; pdb.set_trace()
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

    return render_template(
        'explorer/contracts.html',
        company=company,
        form=form
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
        return jsonify(result), 200
    else:
        return jsonify(result), 403