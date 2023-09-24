#!/usr/bin/python3
"""
Script that display list of states and their cities
and also individual state details
"""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states():
    states = storage.all("State")
    sorted_states = sorted(states.values(), key=lambda state: state.name)
    return render_template('9-states.html', states=sorted_states)


@app.route('/states/<state_id>', strict_slashes=False)
def state_detail(state_id):
    state = storage.get("State", state_id)
    if state:
        cities = sorted(state.cities, key=lambda city: city.name)
        return render_template('9-states.html', state=state, cities=cities)
    else:
        return "<h1>Not found!</h1>"


@app.teardown_appcontext
def teardown(exception):
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
