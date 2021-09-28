from flask import Flask
from flask_migrate import Migrate, init, migrate, upgrade
from sqlalchemy_utils import database_exists, create_database

from configuration import Configuration
from models import database

application = Flask ( __name__ )
application.config.from_object ( Configuration )

migrateObject = Migrate(application, database)

while(True):
    try:
        if (not database_exists(application.config["SQLALCHEMY_DATABASE_URI"])):
            create_database(application.config["SQLALCHEMY_DATABASE_URI"])

        database.init_app(application)

        with application.app_context() as context:
            init()
            migrate(message="Production migration")
            upgrade()
            break
    except Exception as e:
        print(e)