from flask import Flask, render_template, request, redirect, session, url_for
import re

app = Flask(__name__)
app.debug = True
app.secret_key = 'development key'

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/form", methods = ['POST','GET'])
def form_input():
    print("function hit")
    if request.method == 'POST':
        print("Inside post")
        userInput = str(request.form['searchterm'])
        print(userInput)
        print("After user input")
        if re.match("<(|\/|[^\/>][^>].+|\/[^>][^>]+)>", userInput):
            return render_template('index.html')
        session['userInput'] = userInput
        return redirect(url_for('completed'))
    else:
        return render_template('index.html')

@app.route("/completed")
def completed():
    return render_template("success.html", userInput=session['userInput'])

if __name__ == '__main__':
    app.run("0.0.0.0", "5000")