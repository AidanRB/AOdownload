from flask import Flask, render_template, request, flash
from wtforms import Form, TextField, TextAreaField, validators, StringField, PasswordField, SubmitField
import aoapi

app = Flask(__name__)
app.config['SECRET_KEY'] = '8n2c4804n8n089g63n8093n89038n09g563n980g563'

username = ""
password = ""
loggedin = False

class LoginForm(Form):
    username = StringField('Username:', validators=[validators.required()])
    password = PasswordField('Password:', validators=[validators.required()])

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/login", methods=['GET', 'POST'])
def loginpage(username="", password=""):
    form = LoginForm(request.form)
    if request.method == "POST":
        aoapi.username = request.form["username"]
        aoapi.password = request.form["password"]
        if form.validate():
            flash(aoapi.gatherCredentials())
            #gatherCredentials()
            #return login
        else:
            flash("Please enter both username and password")

    return render_template("login.html", form=form)

@app.route("/thread/<int:tid>/<int:page>")
def showThread(tid, page):
    authors, times, posts = aoapi.getPage(tid, page)
    return render_template("thread.html", tid=tid, page=page, authors=authors, times=times, posts=posts)

if __name__ == "__main__":
    app.run()
