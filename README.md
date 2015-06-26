Wexplorer has been folded into the [Pittsburgh Purchasing Suite](https://github.com/codeforamerica/pittsburgh-purchasing-suite) and is no longer being maintained.

W:/Explorer
---

W-Drive Online

W:/Explorer (or just wexplorer) is [Team Pittsburgh's](http://www.codeforamerica.org/governments/pittsburgh/) digitization effort of a list of City of Pittsburgh contracts that started out as an Excel spreadsheet on the City's shared W-Drive.

#### Current Features
+ Quick search of company names & contract descriptions
+ Contract & company pages with more information about contracts/companies/contacts
+ Ability to add lists of items purchased from these contracts

#### Planned & In Development Features
+ Crowdsourced metadata about contracts

Quickstart
----------

It is highly recommended that you use use [virtualenv](https://readthedocs.org/projects/virtualenv/) (and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) for convenience). For a how-to on getting set up, please consult this [howto](https://github.com/codeforamerica/howto/blob/master/Python-Virtualenv.md).

Then run the following commands to bootstrap your environment. You will need to make sure that you have a database to work with and that it is configured properly. If you don't include information about how to configure the database in your environment, wexplorer will look for a db named `w_drive`.

    # clone the repo
    git clone https://github.com/bsmithgall/wexplorer
    # change into the repo directory
    cd wexplorer
    # install python dependencies
    pip install -r requirements.txt
    # upgrade your database to the latest version
    python manage.py db upgrade
    # run the server
    python manage.py server

NOTE: If this is the first time that you are working with wexplorer, be sure to run the following command (before starting your server) to stamp your database and allow for future migrations:

    python manage.py db stamp head

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
