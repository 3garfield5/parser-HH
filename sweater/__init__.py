from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import fake_useragent
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


conn_url = 'postgresql+psycopg2://yourUserDBName:yourUserDBPassword@yourDBDockerContainerName/yourDBName'

engine = create_engine(conn_url)

db_s = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__) # приложение Flask
app.secret_key = 's^sda6da3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///web-site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) # база данных
ua = fake_useragent.UserAgent()

from sweater import models, routes