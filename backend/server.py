from flask import Flask, request, Response, jsonify, session
from scripts.linkedInScraper import LinkedInScraper 
from scripts.filterCandidates import FilterClass
#from scrapy.crawler import CrawlerProcess
#from scrapy.utils.project import get_project_settings
#from RecruiterAI.linkedin.spiders.linkedin_people_profile import LinkedInPeopleProfileSpider
from flask_cors import CORS
import os
import subprocess

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])
app.secret_key = 'WebScraping'
# DO NOT FORGET TO ADD TEXT FILTERING TO AVOID INJECTION


@app.route('/userengine', methods=['GET', 'POST'])
def linkedin():
    if request.method == 'POST':
        URL = request.form['linkedinUrl']
        scraper = LinkedInScraper(URL)
        usernames = scraper.process()
        print(usernames)
        session['usernames'] = usernames
        return Response(status=204)
    elif request.method == 'GET':
        usernames = session.get('usernames')
        return jsonify(usernames)
    return Response(status=204)
@app.route('/recruiter', methods=['GET', 'POST'])
def recruiter():
    if request.method == 'POST':
        if request.headers.get('X-Request-ID') == "User-Input":
            job_position = request.json.get('jobPosition')
            session['job_position'] = job_position
            location = request.json.get('location')
            session['location'] = location
            job_description = request.json.get('jobDescription')
            session['job_description'] = job_description
            domain = request.json.get('domain')
            session['domain'] = domain
            if location == None:
                location = ""
            print(f'job_position: {job_position}, location: {location}, job_description: {job_description}, domain: {domain}')
            usernames = session.get('usernames')
            os.chdir('./RecruiterAI/')
            subprocess.Popen(['scrapy', 'crawl', 'linkedin_people_profile'])
            os.chdir('../')
            return Response(status=204)
        else:
            job_position = session.get('job_position')
            location = session.get('location')
            job_description = session.get('job_description')
            domain = session.get('domain')
            print(f'job_position: {job_position}, location: {location}, job_description: {job_description}, domain: {domain} + cunt')
            item = request.get_json()
            filterObject = FilterClass(item, job_position, location, job_description, domain)
            filterObject.filter()
            return Response(status=204)
@app.route("/")
def homepage():
    return "hi"
if __name__== "__main__":
    app.run(debug=True)