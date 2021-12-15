#Step – 1(import necessary library)
from flask import (Flask, render_template, request, redirect, session)
import LEDLighting, board

lighting = LEDLighting.LEDLighting(board.D18, 100)

#Step – 2 (configuring your application)
app = Flask(__name__)
app.secret_key = 'root'

#step – 3 (creating a dictionary to store information about users)
user = {"username": "root", "password": "raspberry"}

#Step – 4 (creating route for login)
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if(request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')     
        if username == user['username'] and password == user['password']:
            
            session['user'] = username
            return redirect('/dashboard')

        return "<h1>Wrong username or password</h1>"    

    return render_template("login.html")

#Step -5(creating route for dashboard and logout)
@app.route('/dashboard')
def dashboard():
    if('user' in session and session['user'] == user['username']):        
    	return render_template("dashboard.html")

    return '<h1>You are not logged in.</h1>'  

@app.route('/merica', methods = ['POST', 'GET'])
def merica():
    lighting.Merica()
    return render_template("dashboard.html")

@app.route('/christmas', methods = ['POST', 'GET'])
def christmas():
    lighting.Christmas()
    return render_template("dashboard.html")


#Step -6(creating route for logging out)
@app.route('/logout')
def logout():
    session.pop('user')         
    return redirect('/login')

#Step -7(run the app)
if __name__ == '__main__':
    app.run(debug=True)