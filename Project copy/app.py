import os
from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import pandas as pd
import functions as f

UPLOAD_FOLDER = 'static/uploads/'
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
app.config['SECRET_KEY']= 'thisisasecretkey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['csv'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Allow the app and flask login to work together
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model, UserMixin):
    '''
    Represents a user in the Database.
    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class RegisterForm(FlaskForm):
    '''
    Form for user Registration.
    '''
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=25)], render_kw={"placeholder": "Password"})
    
    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = Users.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That Username already exists. Please choose a different one.'
            )

class LoginForm(FlaskForm):
    '''
    Form for user Login.
    '''
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=25)], render_kw={"placeholder": "Password"})
    
    submit = SubmitField('Login') 


class User(db.Model):
    '''
    Represents a Entry in the database.
    '''
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    min_temp = db.Column(db.Float)
    max_temp = db.Column(db.Float)
    rainfall = db.Column(db.Float)
    humidity_9am = db.Column(db.Integer)
    humidity_3pm = db.Column(db.Integer)
    temp_9am = db.Column(db.Float) 
    temp_3pm = db.Column(db.Float)
    pressure_9am = db.Column(db.Float)
    cloud_9am = db.Column(db.Float)
    rain = db.Column(db.Boolean)


@app.route('/')
def home():
    '''
        Renders the Initial page, if authenticated, show upload.html, else go to login page.
    '''
    if current_user.is_authenticated:
        return redirect(url_for('upload_form'))
    else:
        return redirect(url_for('login'))
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    '''
        Renders the registration page
    '''
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = Users(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        # Flash the message with a 'success' category
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
        Renders the login page
    '''
    if current_user.is_authenticated:
        return redirect(url_for('upload_form'))

    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('upload_form'))
            else:
                return render_template('login.html', form=form, error = "Invalid username or password")
        else:
                return render_template('login.html', form=form, error = "Invalid username or password")
            
    return render_template('login.html', form=form)


@app.route('/upload')
@login_required
def upload_form():
    #If data exists already, skip upload page
    if User.query.count() > 0:
        return redirect(url_for('dashboard'))
    return render_template('upload.html')

@app.route("/reset_dataset", methods=["POST"])
@login_required
def reset_dataset():
    # 1) Clear DB rows (weather records)
    db.session.query(User).delete()
    db.session.commit()

    # 2) Clear dataset name from session
    session.pop("dataset_name", None)

    # 3) Delete generated charts (keep australia.jpg)
    img_folder = os.path.join(app.root_path, "static", "img")
    keep = {"australia.jpg"}
    if os.path.isdir(img_folder):
        for fname in os.listdir(img_folder):
            if fname in keep or fname.startswith("."):
                continue
            fpath = os.path.join(img_folder, fname)
            if os.path.isfile(fpath):
                os.remove(fpath)

    flash("Dataset cleared. Please upload a new CSV.", "success")
    return redirect(url_for("upload_form"))

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    file = request.files.get('file')
    if not file or file.filename == '':
        flash('Please choose a CSV file.')
        return redirect(url_for('upload_form'))

    if not allowed_file(file.filename):
        flash('Please only insert csv files.')
        return redirect(url_for('upload_form'))

    filename = secure_filename(file.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(save_path)

    success = f.import_weather_data(save_path, db, User)

    if not success:
        return redirect(url_for("upload_form"))
    db.session.commit()
    session["dataset_name"] = filename
    return redirect(url_for('dashboard'))


# This page will be displayed after the user logs in and inputs the CSV File data.
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    dataset_name = session.get("dataset_name")
    if not dataset_name:
        return redirect(url_for('upload_form'))
    # get distinct city names from DB (example assumes model User with column location)
    cities = [row[0] for row in db.session.query(User.location).distinct().order_by(User.location).all()]
    return render_template('dashboard.html', dataset_name=dataset_name, cities=cities)


@app.route('/dashboard_results')
@login_required
def dashboard_results():
    theme = request.args.get("theme")
    city = request.args.get("city")
    if not theme or not city:
        return render_template(
            "dashboard_results.html",
            theme=theme or "None",
            city=city or "None",
            summary="Please select both a theme and a city.",
            charts=[]
        )
    city_df = f.convert_city_df(city, User)
    if theme == "temperature":
        summary, charts = f.temperature_trends(city_df, city)
    elif theme == "rainfall":
        summary, charts = f.rainfall_patterns(city_df, city)
    elif theme == "extreme":
        summary, charts = f.extreme_indicators(city_df, city)
    else:
        summary, charts = "Unknown theme selected.", []
    return render_template("dashboard_results.html", theme=theme, city=city,summary=summary, charts=charts
)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    '''
        Logs the user out and redirects to the home page. Also deletes the Dataset if uploaded and clears the session
    '''
    filename = session.get("dataset_name")
    if filename:
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        if os.path.exists(file_path):
            os.remove(file_path)

    db.session.query(User).delete()
    db.session.commit()
    session.clear()

    # Delete generated chart images (keep australia.jpg)
    img_folder = os.path.join(app.root_path, "static", "img")
    keep = {"australia.jpg"}

    if os.path.isdir(img_folder):
        for fname in os.listdir(img_folder):
            if fname in keep:
                continue
            # Skip hidden files
            if fname.startswith("."):
                continue

            path = os.path.join(img_folder, fname)
            if os.path.isfile(path):
                os.remove(path)
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    '''
        On first run, this will create the database and import data from the CSV file.
        On subsequent runs, it will skip the import if data already exists to speed up server startup.
    '''
    with app.app_context():
        db.create_all()
        # Deletes all existing records
        db.session.query(User).delete()
        db.session.commit()
        
        
        if User.query.count() == 0:
            print("Database empty. Starting bulk import...")
            db.session.commit()
        else:
            print("Data already exists. Skipping import to start server faster.")
            
    print("Starting Web Server...")
    app.run(debug=True, port=5001)