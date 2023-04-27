from flask import Flask, request, redirect
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def server():
    if request.method == 'POST':
        URL = request.form['linkedinUrl']
        subprocess.run(['python', 'project\backend\ProfileUserEngine-main\main.py', URL])
        return 'Search Began'
    else:
        return 'fail'



if __name__== "__main__":
    app.run(debug=True)