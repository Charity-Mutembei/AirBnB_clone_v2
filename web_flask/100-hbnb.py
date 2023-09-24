#!/usr/bin/python3
"""
changing more for the UI
"""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    states = storage.all("State")
    cities = storage.all("City")
    amenities = storage.all("Amenity")
    places = storage.all("Place")

    sorted_states = sorted(states.values(), key=lambda state: state.name)
    sorted_cities = sorted(cities.values(), key=lambda city: city.name)
    sorted_amenities = sorted(amenities.values(),
                              key=lambda amenity: amenity.name)
    sorted_places = sorted(places.values(), key=lambda place: place.name)

    return render_template(
        '100-hbnb.html',
        states=sorted_states,
        cities=sorted_cities,
        amenities=sorted_amenities,
        places=sorted_places
    )


@app.teardown_appcontext
def teardown(exception):
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
