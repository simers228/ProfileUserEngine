from flask import Flask, request, render_template
import subprocess

app = Flask(__name__, static_folder="../frontend/build/static", template_folder="../frontend/build/static")

@app.route('/', methods=['GET', 'POST'])
def server():
    if request.method == 'POST':
        URL = request.form['linkedinUrl']
        subprocess.run(['python', '.\ProfileUserEngine-main\main.py', URL])
        return render_template("index.html")
    else:
        return 'Failure'



if __name__== "__main__":
    app.run(debug=True)