# Import Dependencies
from flask import Flask, jsonify

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

# Create an app
app = Flask(__name__)


# Define static routes
@app.route("/")
def Home_page():
    
    session = Session(engine)
    
    #List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )

# Define the precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Return a list of all dates and precipitation results

    session = Session(engine)

    # Query all precipitation results
    prcp_results = session.query(Measurement.date, Measurement.prcp).\
        all()

    # Convert to a dict
    all_prcp = dict(prcp_results)

    # Return jsonified results
    return jsonify(all_prcp)

# Define the stations route
@app.route("/api/v1.0/stations")
def stations():
    # Return a list of all stations

    session = Session(engine)

    # Query all stations
    station_results = session.query(Station.id, Station.station).\
        all()

    # Convert to a dict
    all_stations = dict(station_results)

    # Return jsonified results
    return jsonify(all_stations)

# Define the tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    # Return a list of all temperature observations (tobs) in last 12 months
    
    session = Session(engine)

    # Calculate the date 1 year ago from the last data point in the database
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query all tobs for the last year
    tobs_results = session.query(Measurement.id, Measurement.tobs).\
        filter(Measurement.date >= year_ago).order_by((Measurement.date).\
        desc()).\
        all()

    # Convert to a dict
    year_tobs = dict(tobs_results)

    # Return jsonified results
    return jsonify(year_tobs)

# Define the start-date-only route
@app.route("/api/v1.0/start_date/<start_date>")
def start_date(start_date):
    
    session = Session(engine)

    # Query for the min, max and average temperature for the date input
    start_date_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        all()

    # Return jsonified results
    return jsonify(start_date_results)

# Define the start/end -date route
@app.route("/api/v1.0/<start_date>/<end_date>")
def calc_temps(start_date, end_date):
    
    session = Session(engine)

    # Query for the min, max, and average temperature in the date range
    date_range_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).\
        all()

    # Return jsonified results
    return jsonify(date_range_results)

# Define main behavior
if __name__ == "__main__":
    app.run(debug=True)