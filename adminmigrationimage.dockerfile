FROM python:3

RUN mkdir -p /opt/src/admin
WORKDIR /opt/src/admin

COPY admin/migrate.py ./migrate.py
COPY admin/adminDecorator.py ./authDecorator.py
COPY admin/configuration.py ./configuration.py
COPY admin/manage.py ./manage.py
COPY admin/models.py ./models.py
COPY admin/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENTRYPOINT ["sleep", "1200"]
ENTRYPOINT ["python", "./migrate.py"]
