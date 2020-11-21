from flask import Flask
from flask import render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectMultipleField
from wtforms.validators import DataRequired
from mealplan import *

app = Flask(__name__)

users_choices = []
days = 7

def set_choices(choices):
    users_choices = choices

class ChoicesForm(FlaskForm):
    choices = SelectMultipleField('Select Proteins', choices=[(protein,protein) for protein in get_options(meal_plan)], validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET','POST'])
def home():
    form = ChoicesForm()
    if form.validate_on_submit():
        set_choices(form.choices.data)
        return render_template(url_for(meal_plan))
    return render_template('home.html', form=form)


@app.route('/meal-plan')
def meal_plan():
    meal_plan = create_random_meal_plan(meal_plan, users_choices, days)
    return (render_template('mealplan.html', mealplan=meal_plan))


@app.error_handler(404)
def not_found(e):
    return render_template('404.html')

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)