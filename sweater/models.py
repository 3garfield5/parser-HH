from sweater import db

class Vacancy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True, unique=False)
    salary = db.Column(db.String(100), nullable=True, unique=False)
    work_experience = db.Column(db.String(100), nullable=True, unique=False)
    chart = db.Column(db.String(100), nullable=True, unique=False)
    skills = db.Column(db.String(100), nullable=True, unique=False)
    address = db.Column(db.String(100), nullable=True, unique=False)
    link = db.Column(db.String(100), nullable=True, unique=False)
