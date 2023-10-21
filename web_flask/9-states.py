#!/usr/bin/python3
"""List of states and state"""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route("/states", strict_slashes=False)
@app.route("/states/<id>", strict_slashes=False)
def states(id=None):
    states = storage.all(State).values()

    state = None
    if id:
        for st in states:
            if st.id == id:
                state = st

    return render_template("9-states.html", states=states, state=state, id=id)


@app.teardown_appcontext
def teardown(res):
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
