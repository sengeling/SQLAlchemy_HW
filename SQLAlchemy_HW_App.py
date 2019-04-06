# 1. Import Flask
from flask import Flask, jsonify

import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# 2. Create an app
app = Flask(__name__)


# 3. Define static routes
@app.route("/")
def Home_page():
    #List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Return a list of all dates and precipitation results
    # Query all precipitation results
    prcp_results = session.query(Measurement.date, Measurement.prcp).all()

    # Convert list of tuples into normal list
    all_prcp = dict(prcp_results)

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():
    # Return a list of all stations
    # Query all stations
    station_results = session.query(Station.id, Station.station).all()

    # Convert list of tuples into normal list
    all_stations = dict(station_results)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Return a list of all temperature observations (tobs) in last 12 months
    
    # Calculate the date 1 year ago from the last data point in the database
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Query all tobs for the last year
    tobs_results = session.query(Measurement.id, Measurement.tobs).filter(Measurement.date >= year_ago).order_by((Measurement.date).desc()).all()

    # Convert list of tuples into normal list
    year_tobs = dict(tobs_results)

    return jsonify(year_tobs)


# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)