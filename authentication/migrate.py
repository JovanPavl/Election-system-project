from re import match

from flask import Flask, request, Response, jsonify
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, get_jwt_identity, get_jwt, \
    jwt_required
from flask_migrate import Migrate, init, migrate, upgrade
from sqlalchemy import and_
from sqlalchemy_utils import database_exists, create_database

from configuration import Configuration
from models import database, User
from email.utils import parseaddr
from checker import  Checker
from authDecorator import  roleCheck

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

            admin = User(
                jmbg="0000000000000",
                forename="admin",
                surname="admin",
                email="admin@admin.com",
                password="1",
                role = "1"
            );
            database.session.add(admin)
            database.session.commit()
            break
    except Exception as e:
        print(e)