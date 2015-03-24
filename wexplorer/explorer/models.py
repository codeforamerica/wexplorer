# -*- coding: utf-8 -*-

from wexplorer.database import (
    Column,
    db,
    Model,
    relationship
)

from sqlalchemy.dialects.postgresql import UUID
from wexplorer.extensions import bcrypt

class FileUploadPassword(Model):
    __tablename__ = 'file_upload_password'
    password = Column(db.String(128), nullable=False, primary_key=True)

    def __init__(self, password):
        if password:
            self.password = bcrypt.generate_password_hash(password)
        else:
            raise Exception('File Upload Password must be supplied')

class Company(Model):
    __tablename__ = 'company'
    row_id = Column(db.Integer)
    company_id = Column(db.String(32), primary_key=True)
    company = Column(db.String(255))
    bus_type = Column(db.String(255))
    company_contacts = db.relationship('CompanyContact', backref='company', lazy='joined')
    contracts = db.relationship('Contract', backref='company', lazy='joined')

class CompanyContact(Model):
    __tablename__ = 'company_contact'
    row_id = Column(db.Integer)
    company_contact_id = Column(db.String(32), primary_key=True)
    contact_name = Column(db.String(255))
    address_1 = Column(db.String(255))
    address_2 = Column(db.String(255))
    phone_number = Column(db.String(255))
    fax_number = Column(db.String(255))
    email = Column(db.String(255))
    fin = Column(db.String(255))
    company_id = Column(db.String(32), db.ForeignKey('company.company_id'))

class Contract(Model):
    __tablename__ = 'contract'
    row_id = Column(db.Integer)
    contract_id = Column(db.String(32), primary_key=True)
    description = Column(db.Text)
    notes = Column(db.Text)
    county = Column(db.String(255))
    type_of_contract = Column(db.String(255))
    pa = Column(db.String(255))
    expiration = Column(db.DateTime)
    contract_number = Column(db.String(255))
    contract_sub_number = Column(db.Integer)
    controller_number = Column(db.Integer)
    commcode = Column(db.Integer)
    company_id = Column(db.String(32), db.ForeignKey('company.company_id'))
