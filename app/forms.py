from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Optional, Length


NEEDS_CHOICES = [
    ("", "Selecciona una opción"),
    ("observabilidad", "Observabilidad"),
    ("performance", "Pruebas de carga y estrés"),
    ("zentriks", "Plataforma Zentriks"),
    ("cloud", "Cloud y AWS"),
    ("automatizacion", "Automatización e IA"),
    ("integraciones", "Desarrollo e integraciones"),
    ("ams", "AMS y optimización continua"),
    ("moodle", "Moodle Enterprise"),
    ("otro", "Otro"),
]

SIZE_CHOICES = [
    ("", "Selecciona tamaño"),
    ("1-10", "1 – 10"),
    ("11-50", "11 – 50"),
    ("51-200", "51 – 200"),
    ("201-500", "201 – 500"),
    ("500+", "500+"),
]


class ContactoForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=100)])
    empresa = StringField("Empresa", validators=[DataRequired(), Length(max=120)])
    cargo = StringField("Cargo", validators=[Optional(), Length(max=100)])
    email = StringField("Email corporativo", validators=[DataRequired(), Email(), Length(max=120)])
    telefono = StringField("Teléfono", validators=[Optional(), Length(max=20)])
    tamano_empresa = SelectField("Tamaño de empresa", choices=SIZE_CHOICES, validators=[Optional()])
    necesidad = SelectField("¿Qué necesitas resolver?", choices=NEEDS_CHOICES, validators=[Optional()])
    mensaje = TextAreaField("Detalle adicional", validators=[DataRequired()])


class LoginForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired(), Length(max=120)])
    password = PasswordField("Clave", validators=[DataRequired(), Length(min=4, max=128)])
