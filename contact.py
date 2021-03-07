from flask import Flask,render_template,session,redirect,url_for,flash,request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Required
from flask_mail import Mail,Message
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app=Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = "hard to guess" #baghsalbfripfndj
app.config['MAIL_SERVER'] = 'smtp.mail.yahoo.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
migrate = Migrate(app, db)
mail=Mail(app)



class ContactForm(FlaskForm):
    name = StringField('Name',validators = [DataRequired()])
    email = StringField('Email',validators = [DataRequired()])
    pno = StringField('Phone_no',validators = [DataRequired()])
   
    query_msg = TextAreaField('Query',validators = [DataRequired()])
    
    submit = SubmitField('Submit')

class Role(db.Model):
    __tablename__ = 'roles'
    name = db.Column(db.String(64),unique=True)
    pno = db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(64),unique=True)

   # users = db.relationship('User',backref='role',lazy='dynamic')

    def __repr__(self):
        return '<Role %r %r %r>' % (self.name,self.pno, self.email)

class User(db.Model):
    __tablename__ = 'users'
     
    name = db.Column(db.String(64),unique=True)
    pno = db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(64),unique=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.pno'))

    def __repr__(self):
        return '<Role %r %r %r>' % (self.name,self.pno, self.email)

@app.route('/',methods=['GET','POST'])
def index():
    form = ContactForm()
    if form.validate_on_submit():
          
        session['name'] = form.name.data
    
        form.name.data = ''
        
        session['email'] = form.email.data     
        form.email.data = ''

        session['pno'] = form.pno.data
        form.pno.data=''
        
        session['query_msg'] = form.query_msg.data
        form.query_msg.data = ''
      
        
    
        user = User.query.filter_by(email = session['email']).first()
        if user is None:
            user = User(name=session['name'],email=session['email'],pno=session['pno'])
            db.session.add(user)
            db.session.commit()
            flash("Submitted!")
            message = Message("new query", sender = "amitabharoy98@yahoo.com", recipients =session['email'])
            message.body = "Name is" + name + " " +"Phone No" + pno + " "+ "Query is" + query
            mail.send(message)
            


            return redirect(url_for('index'))
    return render_template('index.html', form = form)
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500