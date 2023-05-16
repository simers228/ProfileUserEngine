from flask import Flask, request, Response, jsonify, send_file
from scripts.linkedInScraper import LinkedInScraper
from scripts.filterCandidates import FilterClass
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
# from RecruiterAI.linkedin.spiders.linkedin_people_profile import LinkedInPeopleProfileSpider
from flask_cors import CORS
import os
import subprocess
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlinterface.SQLConnection import PostgresConnection
from loveSosa import loveSosa


app = Flask(__name__)
app.config['SECRET_KEY'] = "My Secret Key"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
CORS(app, origins=['http://localhost:3000'])


# DO NOT FORGET TO ADD TEXT FILTERING TO AVOID INJECTION


@app.route('/userengine', methods=['GET', 'POST'])
def linkedin():
    usernames = ['allisonbentley', 'andrea-wilkins-aa717b151', 'ben-hruban-b18b51b6', 'colin-bailey-a618a622', 'corey-buck-leed-ap-27508910a', 'derrick-hensel-0886996a', 'dustin-parish-a0434468',
                 'j-d-eickbush-53861456', 'jeremy-just-b0003441', 'jessica-florez-909b15a', 'joe-buelt-68923875', 'jon-timperley-454a2754', 'kendal-fuller-4998b797', 'kevin-sladovnik-12a8a72a', 'shane-rothchild-a18610106']
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
            user = request.json.get('user')
            job_position = request.json.get('jobPosition')
            location = request.json.get('location')
            job_description = request.json.get('jobDescription')
            domain = request.json.get('domain')
            if location == None:
                location = ""

            myConn = PostgresConnection()
            myConn.connect()
            updateTable = 'tbl_recruiteroptions'
            valuesList = [user, job_position,
                          location, job_description, domain]
            myConn.insertStatement(updateTable, valuesList)
            myConn.disconnect()

            os.chdir('./RecruiterAI/')
            subprocess.Popen(['scrapy', 'crawl', 'linkedin_people_profile'])
            os.chdir('../')
            return Response(status=204)
        else:
            myConn = PostgresConnection()
            myConn.connect()
            userList = myConn.selectStatement(
                f"SELECT * FROM tbl_recruiteroptions where charuser = \'{user}\';")

            myConn.disconnect()
            print("select list return > \n")
            print(userList)

            # print(
            #     f'job_position: {job_position}, location: {location}, job_description: {job_description}, domain: {domain}')
            item = request.get_json()
            filterObject = FilterClass(
                item, job_position, location, job_description, domain)
            file = filterObject.filter()
            return send_file(file.to_csv('outreach.csv'))


@app.route("/")
def homepage():
    return "hi"


if __name__ == "__main__":
    app.run(debug=True)
