FROM python:3

RUN mkdir -p /opt/src/voting
WORKDIR /opt/src/voting

COPY voting/application.py ./application.py
COPY voting/requirements.txt ./requirements.txt
COPY voting/adminDecorator.py ./adminDecorator.py
COPY voting/models.py ./models.py
COPY voting/configuration.py ./configuration.py

RUN pip install -r ./requirements.txt

ENTRYPOINT ["python", "./application.py"]
