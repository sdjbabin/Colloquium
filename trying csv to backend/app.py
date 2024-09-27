# app.py

from flask import Flask, jsonify, request
from model import db, ResumeInfo
import csv
import os

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

# @app.route('/')
# def home():
#     return "Welcome to the Home Page!"

@app.route('/', methods=['GET'])
# @app.route('/save_resume_info', methods=['POST'])
def save_resume_info():
    csv_file_path = 'resume_info.csv'
    
    if not os.path.exists(csv_file_path):
        return jsonify({"error": "CSV file not found"}), 404
    
    try:
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            
            for row in csv_reader:
                print(f"Processing row: {row}")  # Print the row being processed
                
                resume_info = ResumeInfo(
                    name=row['Name'],
                    skills=row['Skills'],
                    experience=int(row['Experience']),
                    education=row['Education']
                )
                db.session.add(resume_info)
            
            db.session.commit()
            return jsonify({"message": "Resume information stored successfully"}), 201
    
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({"error": str(e)}), 500

   

if __name__ == '__main__':
    app.run(debug=True)
