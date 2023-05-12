from flask import Flask, request, Response, jsonify, flash
import subprocess
import os
import json
import sys
import main
import main_template


app = Flask(__name__)
# DO NOT FORGET TO ADD TEXT FILTERING TO AVOID INJECTION
@app.route('/userengine', methods=['GET', 'POST'])
def linkdein():
    if request.method == 'POST':
        URL = request.form['linkedinUrl']
        main.function(URL)
        return Response(status=204)
@app.route('/usernames', methods=['GET', 'POST'])
def username():
    global usernames
    if request.method == 'POST':
        usernames = request.get_json()
        print(usernames)
    elif request.method == 'GET':
        return jsonify(usernames)
    return Response(status=204)
@app.route('/recruiter', methods=['GET', 'POST', 'OPTIONS'])
def recruiter():
    global job_position, location, job_description, domain
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return Response(headers=headers)
    elif request.method == 'POST':
        job_position = request.json.get('jobPosition')
        location = request.json.get('location')
        job_description = request.json.get('jobDescription')
        domain = request.json.get('domain')
        os.chdir('./RecruiterAI-main/')
        subprocess.Popen(['scrapy', 'crawl', 'linkedin_people_profile'])
        os.chdir('../')
        return Response(status=204)
    elif request.method =='GET':
        return jsonify({'job_position': job_position, 'location': location, "job_description": job_description, 'domain': domain})
@app.route('/jobmodel', methods=['POST'])
def jobmodel():
    if request.method == 'POST':
        item = request.get_json()
        main_template.function(item)
        return Response(status=204)
if __name__== "__main__":
    app.run(debug=True)