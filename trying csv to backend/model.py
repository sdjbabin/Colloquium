# models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ResumeInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    skills = db.Column(db.Text, nullable=False)
    experience = db.Column(db.Integer, nullable=False)  # 1 if experience present, 0 if not
    education = db.Column(db.Text, nullable=False)
