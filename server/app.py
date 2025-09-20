# server/app.py
from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    quake = Earthquake.query.filter_by(id=id).first()
    if quake:
        return jsonify({
            "id": quake.id,
            "location": quake.location,
            "magnitude": quake.magnitude,
            "year": quake.year
        }), 200
    else:
        return jsonify({"message": f"Earthquake {id} not found."}), 404


@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    return jsonify({
        "count": len(quakes),
        "quakes": [
            {
                "id": q.id,
                "location": q.location,
                "magnitude": q.magnitude,
                "year": q.year
            } for q in quakes
        ]
    }), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
