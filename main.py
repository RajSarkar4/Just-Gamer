from flask import Flask, render_template, url_for, flash, request, redirect, Response, jsonify, abort, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from form import LoginForm, RegistrationForm, SoloContestForm, DuoContestForm, SquardContestForm, AddWinnerForm, DefaultForm, ForgotForm
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_wtf import CSRFProtect
from flask_bootstrap import Bootstrap5
from email_verify import Email
from functools import wraps
import pandas as pd
import os

#Initializing Flask application confugiration
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_KEY")
app.config['WTF_CSRF_SECRET_KEY'] = os.environ.get("CSRF_KEY")
app.config['UPLOAD_FOLDER'] = "C:/Users/srajs/Downloads"
csrf = CSRFProtect(app)
csrf.init_app(app)
Bootstrap5(app)
verify = Email()

# Creating Database
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///justgamer.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# User Table
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    discord: Mapped[str] = mapped_column(String(250), nullable=False)
    instagram: Mapped[str] = mapped_column(String(250), nullable=False)
    logo: Mapped[str] = mapped_column(Text, nullable=False)
    mimtype: Mapped[str] = mapped_column(Text, nullable=False)

# Website Data table
class Defaults(db.Model):
    __tablename__ = 'webdata'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    filename: Mapped[str] = mapped_column(Text, nullable=False)
    logo: Mapped[str] = mapped_column(Text, nullable=False)
    mimtype: Mapped[str] = mapped_column(Text, nullable=False)

#Winners Table
class Winner(db.Model):
    __tablename__ = 'winners'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lgame_id: Mapped[str] = mapped_column(String(250), nullable=False)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    team_name: Mapped[str] = mapped_column(String(250), nullable=False)
    logo: Mapped[str] = mapped_column(Text, nullable=False)
    mimtype: Mapped[str] = mapped_column(Text, nullable=False)

# Solo Contest table
class SoloContest(db.Model):
    __tablename__ = 'solo'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lgame_id: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    game_name: Mapped[str] = mapped_column(String(250), nullable=False)
    trophy: Mapped[int] = mapped_column(Integer, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    team_name: Mapped[str] = mapped_column(String(250), unique=True, nullable=True)
    logo: Mapped[str] = mapped_column(Text, nullable=False)
    mimtype: Mapped[str] = mapped_column(Text, nullable=False)


# Duo Contest table
class DuoContest(db.Model):
    __tablename__ = 'duo'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lgame_id: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    lgame_name: Mapped[str] = mapped_column(String(250), nullable=False)
    member_id: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    member_name: Mapped[str] = mapped_column(String(250), nullable=False)
    team_name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    logo: Mapped[str] = mapped_column(Text, nullable=False)
    mimtype: Mapped[str] = mapped_column(Text, nullable=False)

# Squard Contest table
class SquardContest(db.Model):
    __tablename__ = 'squard'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lgame_id: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    lgame_name: Mapped[str] = mapped_column(String(250), nullable=False)
    member1_id: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    member1_name: Mapped[str] = mapped_column(String(250), nullable=False)
    member2_id: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    member2_name: Mapped[str] = mapped_column(String(250), nullable=False)
    member3_id: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    member3_name: Mapped[str] = mapped_column(String(250), nullable=False)
    extra_id: Mapped[str] = mapped_column(String(250), unique=True, nullable=True)
    extra_name: Mapped[str] = mapped_column(String(250), nullable=True)
    team_name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    logo: Mapped[str] = mapped_column(Text, nullable=False)
    mimtype: Mapped[str] = mapped_column(Text, nullable=False)


login_manager = LoginManager()
login_manager.init_app(app)



@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

with app.app_context():
    db.create_all()

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if not current_user.is_authenticated:
            return abort(403)
        elif current_user.id != 1:
            return abort(403)

        # Otherwise continue with the route function
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def home():
    all_winners = db.session.execute(db.select(Winner)).scalars().all()
    return render_template('index.html', title='Home', winners=all_winners)

@app.route('/<id>/<title>')
def get_image(id, title):
    if title == 'solo':
        item = db.session.execute(db.select(SoloContest).filter_by(lgame_id=id)).scalar_one_or_none()
    elif title == 'duo':
        item = db.session.execute(db.select(DuoContest).filter_by(lgame_id=id)).scalar_one_or_none()
    elif title == 'squard':
        item = db.session.execute(db.select(SquardContest).filter_by(lgame_id=id)).scalar_one_or_none()
    elif title == 'winner':
        item = db.session.execute(db.select(Winner).filter_by(lgame_id=id)).scalar_one_or_none()
    elif title=='default':
        item = db.session.execute(db.select(Defaults).filter_by(id=id)).scalar_one_or_none()
    elif title=='user':
        item = db.session.execute(db.select(User).filter_by(id=id)).scalar_one_or_none()

    if item and item.logo:
        img =  Response(item.logo, mimetype=item.mimtype)
        return img
    else:
        return "", 404  # Image not found or news item has no image

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        emil = request.form.get('email')
        password = request.form.get('password')
        result = db.session.execute(db.select(User).where(User.email == emil))
        user = result.scalar()
        if not user:
            flash("That email that not exist, please try again!")
            return redirect(url_for('login'))
        elif not (user.password==password):
            flash("Password incorrect, please try again!")
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html', form=form, current_user=current_user, title='login')

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if request.method == "POST":
        if verify.status == True:
            result = db.session.execute(db.select(User).where(User.email == request.form.get('email'))).scalar()
            if result:
                flash("You've already signed up with this email, login instead!")
                return redirect(url_for('login'))
            if request.form.get('password') != request.form.get('confirm'):
                flash("Password not match!")
                return redirect(url_for('register'))
            pic = get_image(1,'default')
            new_user = User(
                email=request.form.get('email'),
                password=request.form.get('password'),
                name=request.form.get('name'),
                logo=pic.get_data(),
                mimtype=pic.mimetype,
                discord=request.form.get('discord'),
                instagram=request.form.get('instagram'),
            )

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('home'))
        else:
            flash("Invalid Otp!")
            return redirect(url_for('register'))
    return render_template('register.html', form=form, current_user=current_user, title='Register')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route('/contest/<type>', methods=['GET', 'POST'])
def contest(type):
    if current_user.is_authenticated:
        if type == 'solo':
            form = SoloContestForm()
            if form.validate_on_submit():
                
                try:
                    pic = request.files['logo']
                    new_data = SoloContest(
                        lgame_id=form.member1_id.data,
                        game_name=form.game_name.data,
                        trophy=form.trophy.data,
                        year=form.start.data,
                        team_name=form.team_name.data,
                        logo=pic.read(),
                        mimtype=pic.mimetype,
                    )
                    db.session.add(new_data)
                    db.session.commit()
                    return redirect(url_for('joined', type=type))
                except:
                    flash('User already registered ith another group.')
                    return redirect(url_for('contest', type=type))
        elif type == 'duo':
            form = DuoContestForm()
            if form.validate_on_submit():
                try:
                    pic = request.files['logo']
                    new_data = DuoContest(
                        lgame_id=form.member1_id.data,
                        lgame_name=form.member1_name.data,
                        member_id=form.member2_id.data,
                        member_name=form.member2_name.data,
                        team_name=form.team_name.data,
                        logo=pic.read(),
                        mimtype=pic.mimetype,
                    )
                    db.session.add(new_data)
                    db.session.commit()
                    return redirect(url_for('joined', type=type))
                except:
                    flash('User already registered ith another group.')
                    return redirect(url_for('contest', type=type))
        elif type == 'squard':
            form = SquardContestForm()
            if form.validate_on_submit():
                try:
                    pic = request.files['logo']
                    new_data = SquardContest(
                        member1_id=form.member1_id.data,
                        member1_name=form.member1_name.data,
                        member2_id=form.member2_id.data,
                        member2_name=form.member2_name.data,
                        member3_id=form.member3_id.data,
                        member3_name=form.member3_name.data,
                        extra_id=form.member4_id.data,
                        extra_name=form.member4_name.data,
                        team_name=form.team_name.data,
                        logo=pic.read(),
                        mimtype=pic.mimetype,
                    )
                    db.session.add(new_data)
                    db.session.commit()
                    return redirect(url_for('joined', type=type))
                except:
                    flash('User already registered ith another group.')
                    return redirect(url_for('contest', type=type))
        else:
            return "<h1>404 Error!</h1>", 404
        return render_template('contest.html', form=form, title='Contest')
    else:
        return redirect(url_for('login'))


@app.route("/add-winner", methods=['POST', 'GET'])
@admin_only
def add_winner():
    form = AddWinnerForm()
    if form.validate_on_submit():
        pic = get_image(form.member1_id.data, form.title.data.lower())
        new_data = Winner(
            title=form.title.data,
            lgame_id=form.member1_id.data,
            team_name=form.team_name.data,
            logo=pic.get_data(),
            mimtype=pic.mimetype,
        )
        db.session.add(new_data)
        db.session.commit()
        return redirect(url_for('add_winner'))

    return render_template('add-winner.html', form=form)

@app.route('/contest/<type>/joined')
def joined(type):
    return render_template('congrats.html')


def send_otp_email(to_add):
    print(to_add)
    if "@" and "." in  to_add:
        verify.generate()
        verify.send_mail(to_add)
        
    else:
        flash("Type a valid email.")
        return redirect(url_for("register"))
    
    
@app.route('/send_otp', methods=["POST", 'GET'])
def send_otp():
    email = ''
    if request.method == "POST":
        data = request.get_json()
    # Call your Python function here
        email = data.get('email')
    if not email:
        return jsonify({"error": "Email is required!"}), 400
    send_otp_email(email)
    return '', 204


@app.route('/validate_otp', methods=['POST'])
def validate_otp():
    otp = request.json.get('otp')
    
    try:
        
        if int(otp) == verify.otp:
            verify.status = True
            return jsonify({"status": "success", "message": "OTP Verified Successfully!"})
        else:
            return jsonify({"status": "error", "message": "Invalid OTP. Please try again."})
    except Exception:
        return jsonify({"status": "error", "message": "Invalid OTP. Please try again."})
    

@app.route('/defaults', methods=['POST', 'GET'])
@admin_only
def add_defaults():
    form = DefaultForm()
    if form.validate_on_submit():
        pic = request.files['logo']
        new_data=Defaults(
            filename=form.filename.data,
            logo=pic.read(),
            mimtype=pic.mimetype
        )
        db.session.add(new_data)
        db.session.commit()
        return redirect(url_for('add_defaults'))
    return render_template('default.html', form=form)

@app.route('/update-profile/<int:id>', methods=['GET', 'POST'])
def update(id):
    user = db.get_or_404(User, id)
    edit_form = RegistrationForm(
        name=user.name,
        email=user.email,
    )
    if request.method == 'POST':
            pic = request.files['logo']
            print(pic)
            user.name = edit_form.name.data
            user.email = edit_form.email.data
            user.logo = pic.read()
            user.mimtype = pic.mimetype
            db.session.commit()
            return redirect(url_for('home'))

    return render_template('register.html', form=edit_form, is_edit=True)

@app.route('/forgot-password', methods=["GET", "POST"])
def forgot():
    form = ForgotForm()
    if request.method == "POST":
        if request.form['submit'] == "Submit":
            result = db.session.execute(db.select(User).where(User.email == request.form.get('email'))).scalar()
            if result:
                send_otp_email(result.email)
                return redirect(url_for('otp_sec', id=result.id))
            else:
                flash("That email that not exist, please try again!")
                return redirect(url_for('forgot'))
    return render_template('forgot.html', form=form)

@app.route('/forgot-password/<int:id>/otp', methods=["POST", "GET"])
def otp_sec(id):
    form = ForgotForm()
    if request.method == "POST":
        if request.form['submit'] == "Verify":
            if form.otp.data:
                if int(form.otp.data) == verify.otp:
                    verify.status = True
                    return redirect(url_for("reset", id=id))
                else:
                    flash("Invalid OTP, Try Again!")
            else:
                    flash("Invalid OTP, Try Again!")
    return render_template('forgot.html', form=form, is_otp=True)

@app.route('/forgot-password/<int:id>/reset', methods=['POST', 'GET'])
def reset(id):
    form = ForgotForm()
    user = db.get_or_404(User, id)
    if request.method =="POST":
        if verify.status:
            if request.form["submit"] == "Reset":
                if request.form.get('password') == request.form.get('confirm'):
                    user.password = form.password.data
                    db.session.commit()
                    verify.status = False
                    return redirect(url_for('login'))
                else:   
                    flash("Password not match, Try Again!")
                    return redirect(url_for("reset", id=id))
        else:
            return redirect(url_for('forgot'))
    return render_template('forgot.html', verified=True, form=form)


def to_dict(row):
    if row is None:
        return None

    rtn_dict = dict()
    keys = row.__table__.columns.keys()
    for key in keys:
        rtn_dict[key] = getattr(row, key)
    return rtn_dict


@admin_only
@app.route('/excel/<type>', methods=['GET', 'POST'])
def exportexcel(type):
    if type == "solo":
        data = SoloContest.query.all()
    elif type == 'duo':
        data = DuoContest.query.all()
    elif type == "squard":
        data = SquardContest.query.all()
    data_list = [to_dict(item) for item in data]
    df = pd.DataFrame(data_list)
    filename = "contesntents.xlsx"
    print("Filename: "+filename)

    writer = pd.ExcelWriter(filename)
    df.to_excel(writer, sheet_name=type.title)
    writer._save()

    return send_file(filename)

@admin_only
@app.route("/clear/<type>")
def clear_data(type):
    if type == "solo":
        data = db.session.query(SoloContest).delete()
    elif type == "duo":
        data = db.session.query(DuoContest).delete()
    elif type == "squard":
        data = db.session.query(SquardContest).delete()
    db.session.commit()
    return redirect(url_for('home'))

@admin_only
@app.route('/send-mail')
def notify():
    all_mails = db.session.query(User).all()
    for mail in all_mails:
        verify.notify(mail.email)
    return redirect(url_for('home'))
    


if __name__ == "__main__":
    app.run(debug=True)