from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from system.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Потребителско име", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Емейл", validators=[DataRequired(), Email(), Length(min=6, max=50)])
    password = PasswordField("Парола", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Потвърди паролатата", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Регистрация")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError("Това потребителско име е заето. Моля изберете друго потребителско име.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError("Този емейл е зает. Моля изберете друг емейл.")


class LoginForm(FlaskForm):
    email = StringField("Емейл", validators=[DataRequired(), Email()])
    password = PasswordField("Парола", validators=[DataRequired(), Length(min=6)])
    remember = BooleanField("Запомни ме")
    submit = SubmitField("Вход")


class UpdateAccountForm(FlaskForm):
    username = StringField("Потребителско име", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Емейл", validators=[DataRequired(), Email(), Length(min=6, max=50)])
    picture = FileField("Обнови профилна снимка", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Обнови")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()

            if user:
                raise ValidationError("Това потребителско име е заето. Моля изберете друго потребителско име.")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()

            if user:
                raise ValidationError("Този емейл е зает. Моля изберете друг емейл.")


class RecipeForm(FlaskForm):
    title = StringField("Заглавие", validators=[DataRequired()])
    ingredients = TextAreaField("Съставки", validators=[DataRequired()])
    preparation = TextAreaField("Начин на приготвяне", validators=[DataRequired()])
    submit = SubmitField("Публикувай")

