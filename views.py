from flask import render_template, Blueprint, request, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.utils import redirect

from utils.serve_posters import generate_poster_url_dict

main_bp = Blueprint('main', __name__)
from database.user_model import User, user_datastore
from application import login_database


@main_bp.route('/', methods=['GET', 'POST'])
def index():

    return render_template("home.html")


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    print(request.method)

    if request.method == 'POST':
        print("submitted login form")
        ##take data from form
        user_email = request.form.get('email')
        user_username = request.form.get('username')
        user_password = request.form.get('password')

        u = User.query.filter_by(email=user_email).first()
        ## check if user u already exists
        # TODO: implemet hash and salt on passwords
        if u and user_password == u.password:
            login_user(u)
            return redirect(url_for('main.survey'))
        else:
            return "user does not exist"
    return render_template("login.html")


@main_bp.route('/survey', methods=['GET', 'POST'])
@login_required
def survey():
    test_ids = ['tt0103859', 'tt0110443', 'tt0089489','tt0047677', 'tt0340163']
    poster_urls = generate_poster_url_dict(test_ids)
    return render_template("survey.html", poster_urls=poster_urls)


@main_bp.route('/bye')
@login_required
def bye():
    logout_user()
    return render_template("bye.html")


@main_bp.route('/about')
def about():
    return render_template("about.html")


@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_email = request.form.get('email')
        user_name = request.form["name"]
        user_password = request.form.get('password')


        u = User.query.filter_by(email=user_email).first()
        ## check if user u already exists
        if u :
            flash("A user with this email already exists. please log in.")
            return redirect('login')
        else:
            user_datastore.create_user(email=user_email, username=user_name, password=user_password)
            login_database.session.commit()


    return render_template("register.html")


@main_bp.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    return render_template("admin.html")
