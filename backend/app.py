import os
from flask import Flask, request, Response, jsonify, send_file, url_for, redirect
from scripts.linkedInScraper import LinkedInScraper
from scripts.filterCandidates import FilterClass
from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
from RecruiterAI.linkedin.spiders.linkedin_people_profile import LinkedInPeopleProfileSpider
from flask_cors import CORS
import subprocess

# SQL Alchemy dependnecies
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
# Import user defined SQL classes
# Goal is to move away from this
from sql.PostgresCoreConnection import PostgresCoreConnectionClass
from sql.PostgresFlaskConnection import PostgresFlaskConnectionClass


# Initialize the connection class
flaskConnectionVariables = PostgresFlaskConnectionClass()

# Initialize Flask
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = flaskConnectionVariables.getConnectionString()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app, origins=['http://localhost:3000'])

# Create db object for connection to database through Flask
db = SQLAlchemy(app)


# DO NOT FORGET TO ADD TEXT FILTERING TO AVOID INJECTION
@app.route('/signUp')
def signUp():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        date = str(datetime.datetime.now())

        # Flask DB initialization
        add_user_stmnt = tbl_users(
            username=username, password=password, created=date)
        db.session.add(add_user_stmnt)
        db.session.commit()

        # SQL Alchemy core implementation using custom wrapper class
        tbl_users = 'tbl_users'
        user_values = [username, password, date]
        myConn = PostgresCoreConnectionClass()
        myConn.connect()
        myConn.insertStatement(tbl_users, user_values)
        myConn.disconnect()

    return Response(status=204)


@app.route('/users')
def login():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')

        myConn = PostgresCoreConnectionClass()
        result = myConn.selectStatement(
            f'SELECT * FROM tbl_users WHERE username = \'{username}\';')
        if result[1] == password:
            print("password is correct \n")
        else:
            print("something went wrong \n")

        print('{username} + {password}')
    return Response(status=204)


@app.route('/userengine', methods=['GET', 'POST'])
def linkedin():
    linkedinUsernames = ['brandon-irby-1159b715', 'dave-ramsey-9a40bb4', 'ewcampbell', 'jennifer-kim-b123a61', 'jeremy-hill-b7042813',
                         'jim-mangelsen-6569842', 'kalika-sinha-3982b418', 'ken-english-837816a7', 'martyreibold', 'mccampbell-bruce-021642a0']

    # Add usernames to the database
    myConn = PostgresCoreConnectionClass()
    myConn.connect()
    updateTable = 'tbl_linkedinusernames'
    for user in linkedinUsernames:
        valuesList = []
        valuesList.append(user)
        myConn.insertStatement(updateTable, valuesList)
    myConn.disconnect()

    # Process post
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
        user = 'request.json.get'
        if request.headers.get('X-Request-ID') == "User-Input":
            user = 'request.json.get'
            job_position = request.json.get('jobPosition')
            location = request.json.get('location')
            job_description = request.json.get('jobDescription')
            domain = request.json.get('domain')
            prompt = request.json.get('prompt')
            if location == None:
                location = ""

            # Create Core SQL connection to run insert
            myConn = PostgresCoreConnectionClass()
            myConn.connect()
            updateTable = 'tbl_recruiteroptions'
            valuesList = [user, job_position,
                          location, job_description, domain]
            myConn.insertStatement(updateTable, valuesList)
            myConn.disconnect()
            myConn.connect()
            result = myConn.selectStatement(
                'SELECT username FROM tbl_linkedinusernames;')
            myConn.disconnect()
            linkedinUsernames = [row[0] for row in result]
            process = CrawlerProcess()
            spider = LinkedInPeopleProfileSpider(
                linkedinUsernames=linkedinUsernames)
            process.crawl(spider)
            process.start()
            process.stop()
            return Response(status=204)
        else:
            # Core connection
            myConn = PostgresCoreConnectionClass()
            userList = myConn.selectStatement(
                f"SELECT * FROM tbl_recruiteroptions where charuser = \'{user}\';")

            print("\n\n\n\nselect list return >> ")
            print(userList)
            job_position = userList[0][1]
            location = userList[0][2]
            job_description = userList[0][3]
            domain = userList[0][4]
            prompt = userList[0][5]
            print("\n\n\n\nselect list return >> ")
            print(
                f'job_position: {job_position}, location: {location}, job_description: {job_description}, domain: {domain}')
            item = request.get_json()
            filterObject = FilterClass(
                item, job_position, location, job_description, domain, prompt)
            file = filterObject.filter()
            file = file.to_csv
            return send_file(file('outreach.csv'))


@app.route("/")
def homepage():
    return "hi"


if __name__ == "__main__":
    app.run(debug=True)
