from flask import Flask, request, Response, jsonify, send_file
from scripts.linkedInScraper import LinkedInScraper 
from scripts.filterCandidates import FilterClass
#from scrapy.crawler import CrawlerProcess
#from scrapy.utils.project import get_project_settings
#from RecruiterAI.linkedin.spiders.linkedin_people_profile import LinkedInPeopleProfileSpider
from flask_cors import CORS
import os
import subprocess
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

app = Flask(__name__)
app.config['SECRET_KEY'] = "My Secret Key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
CORS(app, origins=['http://localhost:3000'])
db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_description = db.Column(db.String)
    job_position = db.Column(db.String)
    location = db.Column(db.String)
    domain = db.Column(db.String)

# DO NOT FORGET TO ADD TEXT FILTERING TO AVOID INJECTION
@app.route('/userengine', methods=['GET', 'POST'])
def linkedin():
    global usernames
    if request.method == 'POST':
        URL = request.form['linkedinUrl']
        scraper = LinkedInScraper(URL)
        usernames = scraper.process()
        print(usernames)
        return Response(status=204)
    elif request.method == 'GET':
        return jsonify(usernames)
    return Response(status=204)
@app.route('/recruiter', methods=['GET', 'POST'])
def recruiter():
    global job_position, location, job_description, domain
    if request.method == 'POST':
        if request.headers.get('X-Request-ID') == "User-Input":
            job_position = request.json.get('jobPosition')
            location = request.json.get('location')
            job_description = request.json.get('jobDescription')
            domain = request.json.get('domain')
            if location == None:
                location = ""
            user = User(job_position=job_position, location=location, job_description=job_description, domain=domain)
            db.session.add(user)
            db.session.commit()
            os.chdir('./RecruiterAI/')
            subprocess.Popen(['scrapy', 'crawl', 'linkedin_people_profile'])
            os.chdir('../')
            return Response(status=204)
        else:
            user = User.query.order_by(User.id.desc()).first()
            job_position = user.job_position
            location = user.location
            job_description = user.job_description
            domain = user.domain
            print(f'job_position: {job_position}, location: {location}, job_description: {job_description}, domain: {domain}')
            item = request.get_json()
            filterObject = FilterClass(item, job_position, location, job_description, domain)
            file = filterObject.filter()
            return send_file(file.to_csv('outreach.csv'))
@app.route("/")
def homepage():
    return "hi"
if __name__== "__main__":
    app.run(debug=True)