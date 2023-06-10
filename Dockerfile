FROM python:3.10-slim 

WORKDIR /restaurant-app 

RUN pip install Flask flask_restful  flask_sqlalchemy flask_cors psycopg2-binary 

COPY . . 

CMD python server.py  