from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy ( )

class ParticipantElection (database.Model):
    __tablename__ = "participantelection"
    id = database.Column(database.Integer, primary_key=True)
    participantId = database.Column ( database.Integer, database.ForeignKey ( "participants.id" ), nullable = False );
    electionId = database.Column ( database.Integer, database.ForeignKey ( "elections.id" ), nullable = False );
class Participant ( database.Model ):
    __tablename__ = "participants"

    id = database.Column ( database.Integer, primary_key = True )
    name = database.Column ( database.String(256), nullable = False)
    individual = database.Column(database.Boolean, nullable = False)

    elections = database.relationship("Election", secondary=ParticipantElection.__table__, back_populates="participants");

class Election ( database.Model ):
    __tablename__ = "elections"

    id = database.Column ( database.Integer, primary_key = True )
    start = database.Column ( database.DATETIME, nullable = False)
    end = database.Column(database.DATETIME, nullable = False)
    individual = database.Column(database.Boolean, nullable = False)

    participants = database.relationship("Participant", secondary = ParticipantElection.__table__, back_populates = "elections")
    votes = database.relationship("Vote", back_populates = "elections")

class Vote( database.Model):
    __tablename__ = "votes"

    id = database.Column ( database.Integer, primary_key = True )
    guid = database.Column(database.String(256), nullable = False)
    participantJmbg = database.Column(database.String(256), nullable = False)
    electionId = database.Column(database.Integer, database.ForeignKey("elections.id"), nullable = False)
    pollNumber = database.Column(database.Integer, nullable = False)
    reason = database.Column(database.String(256), nullable = False)

    elections = database.relationship("Election", back_populates = "votes")

