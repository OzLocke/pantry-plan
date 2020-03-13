from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Oz'}
    items = [
        {
            'item': "Juice",
            'unit': 'Bottle',
            'quantity': 4,
            'area': 'Fridge'
        },
        {
            'item': "Milk",
            'unit': 'Carton',
            'quantity': 1,
            'area': 'Fridge'
        },
        {
            'item': "Cereal",
            'unit': 'Box',
            'quantity': 2,
            'area': 'Cupboard'
        }
    ]
    return render_template('index.html', title='Home', user=user, items=items)