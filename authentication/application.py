from re import match

from flask import Flask, request, Response, jsonify
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, get_jwt_identity, get_jwt, \
    jwt_required
from sqlalchemy import and_

from configuration import Configuration
from models import database, User
from email.utils import parseaddr
from checker import  Checker
from authDecorator import  roleCheck

application = Flask ( __name__ )
application.config.from_object ( Configuration )

@application.route('/', methods=["GET"])
def hello_world():
    return 'Hello World!'

def checkEmail(email):
    if len(parseaddr(email)) == 0 or match("[^@]+@[^@]+\.[^@]+", email) is None or match('[^@]+@.*\.[a-z]{2,}$', email) is None:
        return False
    return True

@application.route ( "/register", methods = ["POST"] )
def register ( ):
    print("REGISTER\n")
    checker = Checker()
    jmbg = request.json.get("jmbg", "")
    email = request.json.get ( "email", "" )
    password = request.json.get ( "password", "" )
    forename = request.json.get ( "forename", "" )
    surname = request.json.get ( "surname", "" )
    result = checker.checkEmpty(jmbg, forename, surname, email, password)
    if(len(result) != 0):
        return jsonify(message = result), 400

    result = checker.checkJmbg(jmbg)
    if(len(result) != 0):
        return jsonify(message = result), 400

    if (not checkEmail(email)):
        return jsonify(message = "Invalid email."), 400

    result = checker.checkPassword(password)
    if(len(result) != 0):
        return jsonify(message = result), 400

    user = User.query.filter(User.email == email).first()

    if(user):
        return jsonify(message = "Email already exists."), 400

    user = User ( jmbg = jmbg, email = email, password = password, forename = forename, surname = surname, role = 0)
    database.session.add ( user )
    database.session.commit ( )

    #got it ok
    return Response (200)

jwt = JWTManager ( application );
@application.route ( "/login", methods = ["POST"] )
def login ():
    print("LOGIN\n")
    checker = Checker()
    email = request.json.get("email", "")
    password = request.json.get("password", "")
    res = checker.checkLogin(email,password)
    if(len(res) != 0):
        return jsonify (message = res), 400

    if (not checkEmail(email)):
        return jsonify (message =  "Invalid email."), 400

    user = User.query.filter(and_(User.email == email, User.password == password)).first()

    if(not user):
        return jsonify(message = "Invalid credentials."), 400

    additionalClaims = {
            "jmbg": user.jmbg,
            "email": user.email,
            "password": user.password,
            "forename": user.forename,
            "surname": user.surname,
            "role": user.role
    }
    accessToken = create_access_token(identity=user.email, additional_claims=additionalClaims)
    refreshToken = create_refresh_token ( identity = user.email, additional_claims = additionalClaims )

    # return Response ( accessToken, status = 200 );
    return jsonify ( accessToken = accessToken, refreshToken = refreshToken ), 200

@application.route ( "/refresh", methods = ["POST"] )
@jwt_required ( refresh = True )
def refresh ( ):
    print("REFRESH\n")
    identity = get_jwt_identity ( );
    refreshClaims = get_jwt ( );
    additionalClaims = {
            "jmbg": refreshClaims["jmbg"],
            "email": refreshClaims["email"],
            "password": refreshClaims["password"],
            "forename": refreshClaims["forename"],
            "surname": refreshClaims["surname"],
            "role":refreshClaims["role"]
    }
    return jsonify (accessToken = create_access_token ( identity = identity, additional_claims = additionalClaims )), 200

@application.route ( "/delete", methods = ["POST"] )
@roleCheck ( role = "1" )
def deleteUser ( ):
    print("DELETE\n")
    email = request.json.get("email", "")
    if(len(email) == 0):
        return jsonify(message="Field email is missing."), 400
    if (not checkEmail(email)):
        return jsonify (message =  "Invalid email."), 400
    user = User.query.filter(User.email == email).first()
    if(not user):
        return jsonify(message = "Unknown user."), 400

    database.session.delete(user)
    database.session.commit()

    return Response(200)

@application.route("/", methods = ["GET"])
def index():
    return 'Hello world'
if ( __name__ == "__main__" ):
    database.init_app ( application );
    application.run ( debug = True, host = "0.0.0.0",port = 5002 );