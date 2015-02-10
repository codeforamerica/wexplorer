# -*- coding: utf-8 -*-

from wexplorer.database import (
    Column,
    db,
    Model,
    relationship
)

from sqlalchemy.dialects.postgresql import UUID

class Company(Model):
    __tablename__ = 'company'
    row_id = Column(db.Integer)
    company_id = Column(db.String(32), primary_key=True)
    company = Column(db.String(255))
    bus_type = Column(db.String(255))
    company_contacts = db.relationship('CompanyContact', backref='company', lazy='joined')
    contracts = db.relationship('Contract', backref='company', lazy='joined')
    purchased_items = db.relationship('PurchasedItems', backref='company', lazy='joined')

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
    contract_number = Column(db.String(255))
    county = Column(db.String(255))
    type_of_contract = Column(db.String(255))
    pa = Column(db.String(255))
    expiration = Column(db.DateTime)
    spec_number = Column(db.String(255))
    controller_number = Column(db.Integer)
    commcode = Column(db.Integer)
    company_id = Column(db.String(32), db.ForeignKey('company.company_id'))

class PurchasedItems(Model):
    __tablename__ = 'company_purchases'
    row_id = Column(db.Integer, primary_key=True)
    item = Column(db.Text)
    company_id = Column(db.String(32), db.ForeignKey('company.company_id'))

    def __init__(self, item, company_id):
        self.item = item
        self.company_id = company_id
