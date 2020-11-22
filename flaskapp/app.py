from flask import Flask
from flask import render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectMultipleField, widgets
from wtforms.validators import DataRequired
from mealplan import meal_plan, create_random_meal_plan, get_options
import os

#TEMPLATE_DIR = os.path.abspath('../templates')
#STATIC_DIR = os.path.abspath('../static')

app = Flask(__name__)#, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.config['SECRET_KEY'] = 'you-will-never-guess'

users_choices = []
days = 7

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class ChoicesForm(FlaskForm):
    choices =  MultiCheckboxField('Select as many Proteins as you like for your meal plan',choices=[(protein,protein) for protein in get_options(meal_plan)])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET','POST'])
def home():
    form = ChoicesForm()
    if form.validate_on_submit():
        users_choices = form.choices.data
        return render_template(url_for(mealplan))
    return render_template('home.html', form=form)


@app.route('/mealplan')
def mealplan():
    #meal_plan = create_random_meal_plan(meal_plan, users_choices, days)
    return (render_template('mealplan.html'))#, mealplan=meal_plan))


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


