import os
import datetime

from wextractor.extractors import ExcelExtractor
from wextractor.loaders import PostgresLoader
from wexplorer.app import db

def update(target):
    try: 
        data = extract(target)
        load(data, db.engine.url)

        try:
            os.remove(target)
        except OSError:
            pass

        return { 'status': 'success' }

    except Exception, e:
        return {
            'status': 'error',
            'message': str(e)
        }

def extract(target):
    def strip_nbsp(val):
        return unicode(unicode(val).decode('ascii', 'ignore'))

    data = ExcelExtractor(
        target,
        header=[
            'type_of_contract', 'contract_number', 'contract_sub_number', 'pa', 'company',
            'description', 'expiration', 'controller_number', 'address_1',
            'address_2', 'email', 'contact_name', 'phone_number', 'fax_number',
            'notes'
        ],
        dtypes=[
            strip_nbsp, strip_nbsp, int, strip_nbsp, strip_nbsp, strip_nbsp,
            datetime.datetime, int, strip_nbsp, strip_nbsp, 
            strip_nbsp, strip_nbsp, strip_nbsp, strip_nbsp, strip_nbsp
        ]
    )
    return data.extract()

def load(data, db_url):
    '''
    db_url is a sqlalchemy url object
    '''
    user = db_url.username if db_url.username else ''
    print db_url
    loader = PostgresLoader(
        {
            'database': db_url.database, 'user': user, 'host': db_url.host,
            'port': db_url.port, 'password': db_url.password
        },
        [{
            'table_name': 'contract',
            'to_relations': [],
            'from_relations': ['company'],
            'pkey': None,
            'columns': (
                ('description', 'TEXT'),
                ('notes', 'TEXT'),
                ('county', 'VARCHAR(255)'),
                ('type_of_contract', 'VARCHAR(255)'),
                ('pa', 'VARCHAR(255)'),
                ('expiration', 'TIMESTAMP'),
                ('contract_number', 'VARCHAR(255)'),
                ('contract_sub_number', 'INTEGER'),
                ('controller_number', 'INTEGER'),
                ('commcode', 'INTEGER')
            )
        },
        {
            'table_name': 'company_contact',
            'to_relations': [],
            'from_relations': ['company'],
            'pkey': None,
            'columns': (
                ('contact_name', 'VARCHAR(255)'),
                ('address_1', 'VARCHAR(255)'),
                ('address_2', 'VARCHAR(255)'),
                ('phone_number', 'VARCHAR(255)'),
                ('email', 'VARCHAR(255)'),
                ('fax_number', 'VARCHAR(255)'),
                ('fin', 'VARCHAR(255)'),
            )
        },
        {
            'table_name': 'company',
            'to_relations': ['company_contact', 'contract'],
            'from_relations': [],
            'pkey': None,
            'columns': (
                ('company', 'VARCHAR(255)'),
                ('bus_type', 'VARCHAR(255)'),
            )
        }]
    )
    loader.load(data, True)
    return