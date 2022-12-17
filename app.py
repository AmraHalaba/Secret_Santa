import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

#------------------------------------------------------------------------------------------
#INITIALIZE APP
#------------------------------------------------------------------------------------------
app = Flask(__name__)


#------------------------------------------------------------------------------------------
#SETUP DATABASE
#------------------------------------------------------------------------------------------
ENV = 'dev'
if ENV == 'dev':
    app.debug = True #during development
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1Health!Success!1@localhost/santa_cintio'
else:
    app.debug = False #in production
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #to avoid "some" warnings

#Create database object
db = SQLAlchemy(app)

#In terminal:
    #go into python --> type 'python'
    #type 'from app import db'
    #type 'db.create_all()'
    #I get ERROR after this
    #if there were no error I would just type 'exit' to exit 'python' and automaticall get back to 'flask-project'
    #because of error create database with function 'db.create_all()' (at bottom)
    

#Create model Employee
class Employee(db.Model):
    __tablename__ = 'employee'
    id           = db.Column(db.Integer, primary_key=True)
    first_name   = db.Column(db.String(100))
    last_name    = db.Column(db.String(100))
    email        = db.Column(db.String(100), unique=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    #constructor/initializator
    def __init__(self, first_name, last_name, email): #takes in all fields except the id
        self.first_name = first_name
        self.last_name  = last_name
        self.email      = email
        
    #object representation
    def __repr__(self):
        return self.first_name + self.last_name


#------------------------------------------------------------------------------------------
#CREATE ROUTES
#------------------------------------------------------------------------------------------
#Homepage Route
@app.route('/')  #route for homepage so only '/'
def index():
    return render_template('index.html')


#------------------------------------------------------------------------------------------
#All Names Route (Read and Create of CRUD)
@app.route('/all_names', methods=['POST', 'GET'])
def all_names():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name  = request.form['last_name']
        email      = request.form['email']
        # print(first_name, last_name, email)
        if first_name == '' or last_name == '' or email == '':
            return render_template('all_names.html', message="Please enter required fields.")
        if db.session.query(Employee).filter(Employee.first_name == first_name).count() == 0 and db.session.query(Employee).filter(Employee.last_name == last_name).count() == 0:
            data = Employee(first_name, last_name, email)
            db.session.add(data)
            db.session.commit()
            return render_template('success.html')
        return render_template('all_names.html', message=f"You have already entered {first_name} {last_name}.")
    else:
        employees = Employee.query.order_by(Employee.date_created).all()
        return render_template('all_names.html', employees=employees)

#------------------------------------------------------------------------------------------
#Delete Names Route
@app.route('/all_names/delete/<int:id>')
def delete_name(id):
    employee = Employee.query.get_or_404(id)
    
    try:
        db.session.delete(employee)
        db.session.commit()
        return redirect('/all_names')
    except:
        return 'There was a problem deleting that employee. Please, try again.'

#------------------------------------------------------------------------------------------
#Update Names Route
@app.route('/all_names/update/<int:id>', methods=['GET', 'POST'])
def update_name(id):
    employee = Employee.query.get_or_404(id)
    if request.method == "POST":
        employee.first_name = request.form['first_name']
        employee.last_name = request.form['last_name']
        employee.email = request.form['email']
        
        try:
            db.session.commit()
            return redirect('/all_names')
        except:
            return f'There was an issue with updating the {employee.first_name} {employee.last_name}'
    else:
        return render_template('update_name.html', employee=employee)


#------------------------------------------------------------------------------------------
#Add Names Route
@app.route('/add/success', endpoint='success', methods=['GET'])
def success():
    employee = Employee.query.get_or_404(id)
    if request.method == "GET":
        return render_template('success.html', employee=employee)


#------------------------------------------------------------------------------------------
#CREATE DATABASE AND RUN APP
#------------------------------------------------------------------------------------------
if __name__ == '__main__':
    with app.app_context(): #to solve error with SQLAlchemy 3.0 and up 
        db.create_all() #create db
    app.run() #run app