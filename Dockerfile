#BUILD STAGE
FROM python:3.9.18-bookworm
WORKDIR /
COPY ./requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# Installa Flask-Migrate separatamente , rimuovere la riga sotto quando non si usa migrate
RUN pip install Flask-Migrate==3.1.0 

COPY ./setup.py ./setup.py
COPY ./flaskr ./flaskr
RUN pip install -e .


#rimuovere quando non si usa migrate
ENV FLASK_APP=flaskr

#RUN STAGE
#rimuovere flask db upgrade && quando non si usa migrate
CMD ["/bin/bash", "-c", "flask db upgrade && flask --app flaskr run --host=0.0.0.0"]