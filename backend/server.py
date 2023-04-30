from flask import Flask, request, Response
import subprocess

app = Flask(__name__)
# DO NOT FORGET TO ADD TEXT FILTERING TO AVOID INJECTION
@app.route('/', methods=['GET', 'POST'])
def server():
    if request.method == 'POST':
        URL = request.form['linkedinUrl']
        subprocess.run(['python', './ProfileUserEngine-main/main.py', URL])
        return Response(status=204)
    else:
        return 'Failure'

if __name__== "__main__":
    app.run(debug=True)