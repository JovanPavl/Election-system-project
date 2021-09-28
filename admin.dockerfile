FROM python:3

RUN mkdir -p /opt/src/admin
WORKDIR /opt/src/admin

COPY admin/application.py ./application.py
COPY admin/adminDecorator.py ./adminDecorator.py
COPY demon/configuration.py ./configuration.py
COPY admin/manage.py ./manage.py
COPY demon/models.py ./models.py
COPY admin/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENTRYPOINT ["python", "./application.py"]
