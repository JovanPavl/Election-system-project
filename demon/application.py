from flask import Flask
from redis import Redis
from datetime import datetime
import os
import time
from sqlalchemy import and_

from configuration import Configuration
from models import Vote, Election,database

application = Flask ( __name__ )
application.config.from_object ( Configuration )
database.init_app ( application )

#retardirane zone i imidzi vise nmg da verujem
os.environ['TZ'] = 'Europe/Belgrade'
time.tzset()
while(True):
    try:
        with application.app_context() as context:
            with Redis ( host = Configuration.REDIS_HOST ) as redis:
                checkStart = len(redis.lrange ( Configuration.REDIS_VOTES_LIST, 0, 0 ))
                while checkStart == 0:
                    checkStart = len(redis.lrange ( Configuration.REDIS_VOTES_LIST, 0, 0 ))

                fields = redis.lpop(Configuration.REDIS_VOTES_LIST).decode("utf-8")
                args = fields.split(",")

                guid = args[0]
                pollNumber = args[1]
                jmbg = args[2]
                reason = ""

                #mozda ovo budes trebao da optimizujes da prodje kako treba
                current_time = datetime.now()
                curElection = Election.query.filter(and_(current_time >= Election.start, current_time <= Election.end)).first()
                if(not curElection):
                    print('SJEBAO\n')
                    continue

                if(int(pollNumber) > len(curElection.participants)):
                    reason = 'Invalid poll number.'
                checkDuplicate = Vote.query.filter(and_(Vote.guid == guid, Vote.electionId == curElection.id)).all()
                if(checkDuplicate):
                    reason = 'Duplicate ballot.'


                vote = Vote(guid = guid,participantJmbg = jmbg, electionId = curElection.id,pollNumber = pollNumber, reason = reason)
                database.session.add(vote)
                database.session.commit()
    except Exception as e:
        print(e)