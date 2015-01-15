W:/Explorer
---

W-Drive Online

W:/Explorer (or just wexplorer) is [Team Pittsburgh's](http://www.codeforamerica.org/governments/pittsburgh/) digitization effort of a list of City of Pittsburgh contracts that started out as an Excel spreadsheet on the City's shared W-Drive.

#### Current Features
+ Quick search of company names & contract descriptions

#### Planned & In Development Features
+ Contract & company pages with more information about contracts/companies/contacts
+ Crowdsourced metadata about contracts

Quickstart
----------

It is highly recommended that you use use [virtualenv](https://readthedocs.org/projects/virtualenv/) (and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) for convenience). For a how-to on getting set up, please consult this [howto](https://github.com/codeforamerica/howto/blob/master/Python-Virtualenv.md).

First, set your app's secret key as an environment variable. For example, example add the following to `.bashrc` or `.bash_profile`.

    export WEXPLORER_SECRET = 'something-really-secret'

Then run the following commands to bootstrap your environment.


    git clone https://github.com/bsmithgall/wexplorer
    cd wexplorer
    pip install -r requirements.txt
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
    python manage.py server

Deployment
----------

In your production environment, make sure the `WEXPLORER_ENV` environment variable is set to `"prod"`.


Shell
-----

To open the interactive shell, run ::

    python manage.py shell

By default, you will have access to `app`, `db`, and the `User` model.


Running Tests
-------------

To run all tests, run ::

    python manage.py test


Migrations
----------

Whenever a database migration needs to be made. Run the following commmands:
::

    python manage.py db migrate

This will generate a new migration script. Then run:
::

    python manage.py db upgrade

To apply the migration.

For a full migration command reference, run `python manage.py db --help`.
