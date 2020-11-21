from flask import Flask
from flask import render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectMultipleField, widgets
from wtforms.validators import DataRequired
from mealplan import meal_plan, create_random_meal_plan, get_options


app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

users_choices = []
days = 7

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class ChoicesForm(FlaskForm):
    choices =  MultiCheckboxField('Select Proteins', choices=[(protein,protein) for protein in get_options(meal_plan)], validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET','POST'])
def home():
    form = ChoicesForm()
    if request.method =="POST" and form.validate_on_submit():
        users_choices = form.choices.data
        return render_template(url_for(meal_plan))
    return render_template('home.html', form=form)


@app.route('/meal-plan')
def mealplan():
    meal_plan = create_random_meal_plan(meal_plan, users_choices, days)
    return (render_template('mealplan.html', mealplan=meal_plan))


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


