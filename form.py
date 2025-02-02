from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, FileField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField

class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm = PasswordField("Confirm Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    discord = StringField("Discord", validators=[DataRequired()])
    instagram = StringField("Instagram", validators=[DataRequired()])
    otp = StringField("Verify OTP", validators=[DataRequired()])
    submit = SubmitField("Sign up")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

class SoloContestForm(FlaskForm):
    member1_id = StringField("GameId", validators=[DataRequired()])
    game_name = StringField("In-Game Name", validators=[DataRequired()])
    trophy = StringField("Trophy", validators=[DataRequired()])
    start = StringField('Started Year', validators=[DataRequired()])
    team_name = StringField("Team Name (Optional)")
    logo = FileField('Logo', validators=[DataRequired()])
    submit = SubmitField('Submit')

class DuoContestForm(FlaskForm):
    member1_id = StringField("Leader GameId", validators=[DataRequired()])
    member1_name = StringField("Leader In-Game Name", validators=[DataRequired()])
    member2_id = StringField("Teammate GameId", validators=[DataRequired()])
    member2_name = StringField("Teammate In-Game Name", validators=[DataRequired()])
    team_name = StringField("Team Name", validators=[DataRequired()])
    logo = FileField('Logo', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SquardContestForm(FlaskForm):
    member1_id = StringField("Leader GameId", validators=[DataRequired()])
    member1_name = StringField("Leader In-Game Name", validators=[DataRequired()])
    member2_id = StringField("Member-1 GameId", validators=[DataRequired()])
    member2_name = StringField("Member-1 In-Game Name", validators=[DataRequired()])
    member3_id = StringField("Member-2 GameId", validators=[DataRequired()])
    member3_name = StringField("Member-2 In-Game Name", validators=[DataRequired()])
    member4_id = StringField("Extra Member GameId (Optional)")
    member4_name = StringField("Extra Member In-Game Name (Optional)")
    team_name = StringField("Team Name", validators=[DataRequired()])
    logo = FileField('Logo', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AddWinnerForm(FlaskForm):
    title = SelectField("Title", validators=[DataRequired()], choices=['Select', 'Solo', 'Duo', 'Squard'])
    member1_id = StringField("Leader Game Id", validators=[DataRequired()])
    team_name = StringField("Team Name", validators=[DataRequired()])
    submit = SubmitField('Submit')

class DefaultForm(FlaskForm):
    filename = StringField("FileName", validators=[DataRequired()])
    logo = FileField('Image', validators=[DataRequired()])
    submit = SubmitField("Submit")

class ForgotForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    otp = StringField("Verify OTP")
    password = PasswordField("Password")
    confirm = PasswordField("Confirm Password")
    submit = SubmitField("Sign up")

