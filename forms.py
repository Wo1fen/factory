from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField
from wtforms.fields import SelectField
from wtforms.fields.html5 import DateTimeField
from wtforms.validators import DataRequired, Length, ValidationError
from datetime import datetime

class ClientForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Имя', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    phone = StringField('Телефон', validators=[DataRequired()])
    submit = SubmitField('Отправить')


class OrderForm(FlaskForm):
    id = HiddenField('id')
    id_client = SelectField('Клиент', validators=[DataRequired()], coerce=int)
    ordate = DateTimeField('Дата заказа', validators=[DataRequired()], default=datetime.now())
    track_number = StringField('Трек')
    submit = SubmitField('Отправить')

class FactoryForm(FlaskForm):
    id = HiddenField('id')
    address = StringField('Адрес', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Отправить')


class ProductionForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Имя', validators=[DataRequired(), Length(max=50)])
    type = StringField('Тип', validators=[DataRequired(), Length(max=50)])
    price = StringField('Цена', validators=[DataRequired()])
    submit = SubmitField('Отправить')

    def validate_price(form, field):
        validate_type(field.data, float, 'Цена должна быть числом!')


class WorkerForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Имя', validators=[DataRequired(), Length(max=50)])
    id_workshop = SelectField('Цех', validators=[DataRequired()], coerce=int)
    id_position = SelectField('Должность', validators=[DataRequired()], coerce=int)
    hire_date = DateTimeField('Дата принятия', validators=[DataRequired()], default=datetime.now())
    qualification = StringField('Квалификации', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Отправить')


class ReleaseForm(FlaskForm):
    id = HiddenField('id')
    id_production = SelectField("Продукт", validators=[DataRequired()], coerce=int)
    weight = StringField('Вес', validators=[DataRequired(), Length(max=50)])
    rdate = DateTimeField('Дата выпуска', validators=[DataRequired()], default=datetime.now())
    id_workshop = SelectField('Цех', validators=[DataRequired()], coerce=int)
    count = StringField('Количество', validators=[DataRequired(), Length(max=50)])
    id_order = SelectField("Заказ", validators=[DataRequired()], coerce=int)
    submit = SubmitField('Отправить')

    def validate_count(form, field):
        validate_type(field.data, int, 'Количество должно быть числом!')
    
    def validate_weight(form, field):
        validate_type(field.data, int, 'Вес должен быть числом!')


class WorkshopForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Имя', validators=[DataRequired(), Length(max=50)])
    id_factory = SelectField('Завод', validators=[DataRequired()], coerce=int)
    id_manager = SelectField('Менеджер', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Отправить')


class PositionForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Название должности', validators=[DataRequired()])
    salary = StringField('Зарплата', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Отправить')

    def validate_salary(form, field):
        validate_type(field.data, int, 'Зарплата должна быть числом!')

def validate_type(value, value_type, message):
    try:
        value_type(value)
    except ValueError:
            raise ValidationError(message)
