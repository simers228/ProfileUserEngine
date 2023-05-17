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


app = Flask(__name__)
app.config['SECRET_KEY'] = "My Secret Key"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
CORS(app, origins=['http://localhost:3000'])


# DO NOT FORGET TO ADD TEXT FILTERING TO AVOID INJECTION

@app.route('/users')
def login():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        date = str(datetime.datetime.now())

        tbl_users = 'tbl_users'
        user_values = [username, password, date]
        myConn = PostgresConnection()
        myConn.connect()
        myConn.insertStatement(tbl_users, user_values)
        myConn.disconnect()

        print('{username} + {password}')
    return Response(status=204)


@app.route('/userengine', methods=['GET', 'POST'])
def linkedin():
    global linkedinUsernames
    if request.method == 'POST':
        URL = request.form['linkedinUrl']
        scraper = LinkedInScraper(URL)
        linkedinUsernames = scraper.process()
        print(linkedinUsernames)
        return Response(status=204)
    elif request.method == 'GET':
        return jsonify(linkedinUsernames)
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
            print("\n\n\n\nselect list return >> ")
            print(userList)

            # print(
            #     f'job_position: {job_position}, location: {location}, job_description: {job_description}, domain: {domain}')
            item = request.get_json()
            filterObject = FilterClass(
                item, job_position, location, job_description, domain)
            file = filterObject.filter()
            file = file.to_csv
            return send_file(file('outreach.csv'))


@app.route("/")
def homepage():
    return "hi"


if __name__ == "__main__":
    app.run(debug=True)
