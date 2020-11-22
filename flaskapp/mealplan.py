import random
import json


def import_file(file_name):
    ##Importing the JSON meal plan file
    with open(file_name, 'r') as file:
        meal_plan = json.load(file)
    return meal_plan


def get_options(json_plan):

    '''This function converts the height in cm to feet and inches 
    Args: takes meal plan dictionary in format (day-> mealtime-> options->[ list of meals]).
    result: Returns a list of all available protein options available in the meal plan.'''

    choices=[]
    for day, _ in json_plan.items():
        for _, data in json_plan[day].items():
            if data.get('Options'):
                for option in data.get('Options'):
                    choices.append(option)
    choices.sort()
    return(sorted(set(choices)))


def get_random_day(meal_plan):
    '''This function picks a day from the list of days in the meal plan. 
    This function also uses the random function from the python library.
    Args: takes meal plan dictionary in format (day-> mealtime-> options-> [ list of meals]).
    result: Returns a random day (string )from the meal_plan.
    '''
    return random.choices(list(meal_plan.keys()))[0]


def get_random_meal_from(data,search):
    '''This function picks a random meal from a dictionary given the search criteria. 
    This function also uses the random function from the python library.
    Args: 1.Takes a meal plan dictionary in format (day-> mealtime-> options->[ list of meals]).
          2.Takes search key option  
    result: Returns a random meal (string) from the data.
    '''
    meal = data.get(search)
    #generate a random integer between 0 and X. random.randint will return 0 if X is 0.
    meal_type = random.randint(0, len(meal)-1)
    #return a meal using the meal_type value
    return meal[meal_type]

import random

def create_random_meal_plan(meal_plan, users_choices, days):
    '''This creates a meal plan from the meal_plan  dictionary
    Args: 1. takes meal plan dictionary in format (day-> meal-> options->[ list of meals]).
          2. takes the users choices as a list of proteins.
          3. takes the number of days (integer) to randomize the meal plan for.
    result: Returns a dictionary in format (day-> mealtime-> meal).
    '''

    custom_meal_plan = {}
    meal_sets = ['Breakfast', 'Lunch', 'Dinner', 'Snacks']
    
    for daycount in range(days): #number of days to generate the meal plan for
        if not custom_meal_plan.get(daycount): #if the day does not exist yet create day
            custom_meal_plan[daycount] = {}    
        
        for meal in meal_sets: #go through the mealtimes (breakfast, lunch, dinner, snacks)
            rand_day = get_random_day(meal_plan) #get the meal info from a random day from the meal_plan
            meal_info = meal_plan[rand_day][meal]

            if meal_info.get('Options'):
                choices = [option for option in meal_info.get('Options') if option in users_choices]
                
                #check if the options match with the users selected protein choices, pick one at random.
                if choices:
                    choice = random.choices(choices)[0]
                    custom_meal_plan[daycount][meal] = get_random_meal_from(meal_info,choice)

                else:
                    #if the choices do not match with the users selected protein options, go with the default meal
                    custom_meal_plan[daycount][meal] = get_random_meal_from(meal_info,'Default')
            else:
                #if there are no options go with the default meal
                custom_meal_plan[daycount][meal] = get_random_meal_from(meal_info,'Default')
    return custom_meal_plan

meal_plan = import_file('meal_plan.json')

if __name__ == '__main__':
    meal_plan = import_file('meal_plan.json')
    plan = create_random_meal_plan(meal_plan, ['Egg','Beef','Chicken','Turkey','Fish'], 7)
    print(plan)

