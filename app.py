from enum import unique
from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, IntegerField
from wtforms import validators
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from datetime import date
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.widgets import TextArea


# Create a Flask Instance
app = Flask(__name__)
# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# Secret Key!
app.config['SECRET_KEY'] = "My super secret key that no one is supposed to know"
SQLALCHEMY_TRACK_MODIFICATIONS = False
# Initialize The Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Create Modal
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    # Do some password stuff!
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute!')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def veryfy_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Create a String
    def __repr__(self):
        return '<Name %r>' % self.name


# Create a Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a Form Class
class PasswordForm(FlaskForm):
    email = StringField("What's Your Email", validators=[DataRequired()])
    password_hash = PasswordField("What's Your Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create a Route Model
class Routes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    truck_id = db.Column(db.Integer)
    driver = db.Column(db.String(255))
    customer = db.Column(db.String(255))
    loading = db.Column(db.String(255))
    unloading = db.Column(db.String(255))
    received = db.Column(db.Integer)
    price = db.Column(db.Integer)
    payment = db.Column(db.String(15))
    debt = db.Column(db.Integer)
    comment = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    
# Create a Routes Form
class RouteForm(FlaskForm):
    truck_id = IntegerField("Truck id", validators=[DataRequired()])
    driver = StringField("Driver", validators=[DataRequired()])
    customer = StringField("Customer", validators=[DataRequired()])
    loading = StringField("Loading point", validators=[DataRequired()])
    unloading = StringField("Unloading point", validators=[DataRequired()])
    received = IntegerField("Received amount", validators=[DataRequired()])
    price = IntegerField("Shipping price", validators=[DataRequired()])
    payment = StringField("Payment", validators=[DataRequired()])
    debt = IntegerField("Debt", validators=[DataRequired()])
    comment = StringField("Comment", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Submit")

# Add Post Page
@app.route('/add-route', methods=['GET', 'POST'])
def add_route():
    form = RouteForm()

    if form.validate_on_submit():
        route = Routes(truck_id=form.truck_id.data, driver=form.driver.data, customer=form.customer.data, loading=form.loading.data, unloading=form.unloading.data, received=form.received.data, price=form.price.data, payment=form.payment.data, debt=form.debt.data, comment=form.comment.data)
        # Clear the Form
        form.truck_id.data = ''
        form.driver.data = ''
        form.customer.data = ''
        form.loading.data = ''
        form.unloading.data = ''
        form.received.data = ''
        form.price.data = ''
        form.payment.data = ''
        form.debt.data = ''
        form.comment.data = ''

        # Add route data to database
        db.session.add(route)
        db.session.commit()

        # Return a Message
        flash("Route Submitted Successfully!")

    # Redirect to the webpage
    return render_template("add-route.html", form=form)



# Update Database Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("update.html", form=form, name_to_update=name_to_update)
        except:
            flash("Error! Looks like there was a problem...try again!")
            return render_template("update.html", form=form, name_to_update=name_to_update)
    else:
        return render_template("update.html", form=form, name_to_update=name_to_update, id=id)
    

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    # Validate Form
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data)
            # Hash the password!!!
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash.data = ''

        flash("User Added Successfully")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form=form, name=name, our_users=our_users)


@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully!")
        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html", form=form, name=name, our_users=our_users)
    except:
        flash("Whoops! There was a problem deleting user, try again...")
        return render_template("add_user.html", form=form, name=name, our_users=our_users)

# Create a route decorator
@app.route('/')
def index():
    firt_name = "Victory"
    stuff = "This is bold text"
    flash("Welcome To Our Website!")
    favorite_pizza = ["Pepperoni", "Cheese", "Mushrooms", 41]
    return render_template("index.html", firt_name=firt_name, stuff=stuff, favorite_pizza=favorite_pizza)


@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)

# Create Password Test Page
@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None

    form = PasswordForm()

    # Validate Form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        # Clear the form
        form.email.data = ''
        form.password_hash.data = ''

        # Lookup User By Email Address
        pw_to_check = Users.query.filter_by(email=email).first()

        # Check Hashed assword
        passed = check_password_hash(pw_to_check.password_hash, password)

    return render_template("test_pw.html", email = email, password = password, 
            pw_to_check = pw_to_check, passed = passed, form = form)


# Create Custom Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Error URL
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

