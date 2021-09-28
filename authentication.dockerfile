FROM python:3

RUN mkdir -p /opt/src/authentication
WORKDIR /opt/src/authentication

COPY authentication/application.py ./application.py
COPY authentication/authDecorator.py ./authDecorator.py
COPY authentication/checker.py ./checker.py
COPY authentication/configuration.py ./configuration.py
COPY authentication/manage.py ./manage.py
COPY authentication/models.py ./models.py
COPY authentication/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENTRYPOINT ["python", "./application.py"]
