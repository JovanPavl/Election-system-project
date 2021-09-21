import re

from dateutil.parser import parse, isoparse
from flask import Flask, request, Response, jsonify

from datetime import datetime

from sqlalchemy import and_, or_

from admin.models import Participant, database, Election, Vote, ParticipantElection
from adminDecorator import roleCheck
from configuration import  Configuration
from flask_jwt_extended import JWTManager

application = Flask ( __name__ )
application.config.from_object ( Configuration )
jwt = JWTManager ( application )

@application.route ( "/createParticipant", methods = ["POST"] )
@roleCheck ( role = "1" )
def createParcipant ( ):
    name = request.json.get("name", "")
    individual = request.json.get("individual", "")
    if(name == ""):
        return jsonify (message = "Field name is missing."), 400
    if(individual == ""):
        return jsonify (message = "Field individual is missing."), 400

    par = Participant(name = name, individual = individual)
    database.session.add (par)
    database.session.commit ( )

    return jsonify(id = par.id), 200

@application.route ( "/getParticipants", methods = ["GET"] )
@roleCheck ( role = "1" )
def getParticipants():
    arr = []
    pars = Participant.query.all()
    for p in pars:
        arr.append({'id':p.id, 'name':p.name, 'individual':p.individual})
    return jsonify(participants = arr), 200

def checkDate(test):
    try:
        isoparse(test)
    except:
        return False
    return True

@application.route ( "/createElection", methods = ["POST"] )
@roleCheck ( role = "1" )
def createElections():
    start = request.json.get("start", "")
    end = request.json.get("end", "")
    individual = request.json.get("individual","")
    participants = request.json.get("participants","")
    if(start == ""):
        return jsonify(message = "Field start is missing."), 400
    if(end == ""):
        return jsonify(message = "Field end is missing."), 400
    if(individual == ""):
        return jsonify(message="Field individual is missing."), 400
    if(participants == ""):
        return jsonify(message="Field participants is missing."), 400

    if(start > end or (not checkDate(start)) or (not checkDate(end))):
        return jsonify(message = "Invalid date and time."), 400

    election = Election.query.filter(or_(and_(isoparse(start) >= Election.start, isoparse(start) <= Election.end)
                                         , and_(isoparse(end) >= Election.start, isoparse(end) <= Election.end))).first()
    if election:
        return jsonify(message = "Invalid date and time."), 400

    parcts = Participant.query.all()
    tmp = []
    for p in parcts:
        if((p.id in participants)):
            tmp.append(p)

    parcts = tmp
    if(len(parcts) < 2):
        return jsonify(message = "Invalid participants."), 400
    list = []
    sol = []
    i = 1
    for p in parcts:
        if(p.individual != individual):
            return jsonify(message="Invalid participants."), 400
        sol.append(i)
        i = i + 1

    elec = Election(start = isoparse(str(start)), end = isoparse(str(end)), individual = individual, participants = parcts)

    database.session.add (elec)
    database.session.commit ( )
    return jsonify(pollNumbers = sol)

@application.route ( "/getElections", methods = ["GET"] )
@roleCheck ( role = "1" )
def getElections():
    sol = []
    elections = Election.query.all()
    for e in elections:
        pars = []
        for p in e.participants:
            pars.append({'id': p.id, 'name': p.name})
        sol.append({
            'id': e.id,
            'start': str(e.start),
            'end': str(e.end),
            'individual': e.individual,
            'participants': pars
        })
    return jsonify(elections=sol),200

@application.route("/getResults", methods=["GET"])
@roleCheck(role = "1")
def getResults():
    id = request.args.get("id")
    if(not id):
        return jsonify(message='Field id is missing.'), 400

    current_time = datetime.now()
    curElection = Election.query.filter(id == Election.id).first()
    if(not curElection):
        return jsonify(message = 'Election does not exist.'),400
    if(curElection.end >= current_time and curElection.start >= current_time):
        return jsonify(message = 'Election is ongoing.'),400

    votes = Vote.query.filter(curElection.id == Vote.electionId).all()
    partcs = ParticipantElection.query.filter(ParticipantElection.electionId == curElection.id).all()

    poolRange = len(partcs)
    curVal = []
    numVotes = []
    numMandats = []

    for i in range (0, poolRange + 1):
        numVotes.append(0)
        numMandats.append(0)
        curVal.append(0)


    badVotes = []

    sumVotes = 0
    for v in votes:
        if(v.reason == ''):
            sumVotes = sumVotes + 1
            numVotes[v.pollNumber] = numVotes[v.pollNumber] + 1
        else:
            badVotes.append(v)

    for i in range(1,poolRange + 1):
        print("LOL" + str(numVotes[i]) + "")

    maks = 0
    poolMaks = 0

    if(not curElection.individual):
       for j in range(1, 251):
           for i in range(1, poolRange + 1):
               curVal[i] = float(numVotes[i])/float(numMandats[i] + 1)
               if(curVal[i] > poolMaks and numVotes[i] >= sumVotes * 0.05):
                   poolMaks = curVal[i]
                   maks = i
           numMandats[maks] = numMandats[maks] + 1
           poolMaks = 0
           maks = 0
    else:
        for i in range(1, poolRange + 1):
            numMandats[i] = float(numVotes[i]) / float(sumVotes)
            numMandats[i] = round(numMandats[i], 2)
            print("LOL " + str(numMandats[i]))
    partcSol = []
    for i in range (0,poolRange):
        tmpParc = Participant.query.filter(Participant.id == partcs[i].participantId).first()
        partcSol.append({'pollNumber': i + 1, "name":tmpParc.name, "result": numMandats[i + 1]})
    invalidVotes = []
    for v in badVotes:
        invalidVotes.append({"electionOfficialJmbg":v.participantJmbg,
                                "ballotGuid":v.guid,
                                "pollNumber":v.pollNumber,
                                "reason":v.reason})

    return jsonify(participants=partcSol, invalidVotes = invalidVotes)
if ( __name__ == "__main__" ):
    database.init_app ( application )
    application.run ( debug = True, port = 5001 );
