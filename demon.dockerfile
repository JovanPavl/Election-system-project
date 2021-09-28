FROM python:3

RUN mkdir -p /opt/src/demon
WORKDIR /opt/src/demon

COPY demon/application.py ./application.py
COPY demon/requirements.txt ./requirements.txt
COPY demon/configuration.py ./configuration.py
COPY demon/models.py ./models.py

RUN pip install -r ./requirements.txt

ENTRYPOINT ["python", "./application.py"]
