from flask import Flask
from flask import render_template, redirect, url_for, request, redirect, flash, session
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectMultipleField, widgets
from wtforms.validators import DataRequired
from mealplan import meal_plan, create_random_meal_plan, get_options
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

csrf = CSRFProtect(app)

days = 28

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class ChoicesForm(FlaskForm):
    choices =  MultiCheckboxField('Select as many Proteins as you like for your meal plan',choices=[(protein,protein) for protein in get_options(meal_plan)])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
def home():
    form = ChoicesForm()
    optionlength = len(get_options(meal_plan))
    if request.method == 'POST':
        if form.validate_on_submit():
            users_choices = form.choices.data
            print(users_choices)
            session['users_choices'] = users_choices
            return redirect(url_for('mealplan'))
        else:
            flash("Validation Failed")
            print(form.errors)
    return render_template('home.html', form=form, options=optionlength)


@app.route('/mealplan')
def mealplan():
    users_choices = session['users_choices']
    meal_planned = create_random_meal_plan(meal_plan, users_choices, days)
    order=['Breakfast','Lunch','Dinner','Snacks']
    return (render_template('mealplan.html', mealplan=meal_planned, mealorder=order))


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5001)