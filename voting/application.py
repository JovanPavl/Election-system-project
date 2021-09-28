from flask import Flask, request, Response, jsonify
import io
import csv
from redis import Redis

from models import database
from adminDecorator import roleCheck
from configuration import  Configuration

from flask_jwt_extended import JWTManager, get_jwt, \
    jwt_required

application = Flask ( __name__ )
application.config.from_object ( Configuration )
jwt = JWTManager ( application )

@application.route ( "/vote", methods = ["POST"] )
@roleCheck ( role = "0" )
@jwt_required ()
def vote():
    claims = get_jwt()
    try:  request.files["file"] == ''
    except Exception:
        return jsonify(message = 'Field file is missing.'), 400

    content = request.files["file"].stream.read ( ).decode ( "utf-8" )
    stream = io.StringIO ( content )
    reader = csv.reader ( stream )


    cnt = 0
    jmbg = claims['jmbg']
    #check if everything is ok
    moja = []
    for row in reader:
        moja.append(row)
        if(len(row) != 2):
            return jsonify(message = 'Incorrect number of values on line ' + str(cnt) + "."), 400
        if(not row[1].isnumeric()):
            return jsonify(message='Incorrect poll number on line ' + str(cnt) + "."), 400
        tmp = int(row[1])
        if(tmp < 0):
            return jsonify(message = 'Incorrect poll number on line ' + str(cnt) + "."), 400
        print(str(row[0]) + " " + str(row[1]) + " " + str(jmbg))
        cnt = cnt + 1

    jmbg = claims['jmbg']
    i = 0
    for row in moja:
        try:
            with Redis(host=Configuration.REDIS_HOST) as redis:
                redis.rpush(Configuration.REDIS_VOTES_LIST,"{},{},{}".format(row[0],int(row[1]),jmbg))
        except Exception as e:
              print(e)

    return Response(200)

if ( __name__ == "__main__" ):
    database.init_app ( application );
    application.run ( debug = True, host = "0.0.0.0", port = 5003 );