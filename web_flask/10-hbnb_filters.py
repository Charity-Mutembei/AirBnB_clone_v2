#!/usr/bin/python3
""""Create a web app to display states as a list"""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    states = storage.all("State")
    cities = storage.all("City")
    amenities = storage.all("Amenity")

    sorted_states = sorted(states.values(), key=lambda state: state.name)
    sorted_cities = sorted(cities.values(), key=lambda city: city.name)
    sorted_amenities = sorted(amenities.values(),
                              key=lambda amenity: amenity.name)

    return render_template('10-hbnb_filters.html',
                           states=sorted_states, cities=sorted_cities,
                           amenities=sorted_amenities)


@app.teardown_appcontext
def teardown(exception):
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
