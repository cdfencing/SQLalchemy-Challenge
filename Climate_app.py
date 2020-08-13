import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

##################################
# Database Setup
##################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect=True)

# Save the references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session from Python to the Database
session = Session(engine)

##################################
# Flask Setup
##################################

app = Flask(__name__)

##################################
# Flask Routes
##################################

@app.route("/")
def welcome():
    return (
        f"<p><b>Welcome! You have reached the Hawaii climate API homepage!</b></p>"
        f"<p><b>Available Routes:</b></p>"
        f"<i>/api/v1.0/precipitation</i><br/>Provides a JSON list of percipitation data for the time period of 8/23/16 through 8/23/17<br/><br/>"
        f"<i>/api/v1.0/stations</i><br/>Provides a JSON list of the Hawaii weather stations<br/><br/>"
        f"<i>/api/v1.0/tobs</i><br/>Provides a JSON list of the Temperature Observations (tobs) data for each individual station for the time period of 8/23/16 through 8/23/17<br/><br/>"
        f"<i>/api/v1.0/date</i> and <i>/api/v1.0/start_date/end_date</i><br/>Provides a JSON list of the minimum and maximum temperature, as well as the average temperature for the time period between the given starting date and end date of 8/23/17<br/><br/>."
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    Precipitation_last_year = session.query(Measurement.date, func.avg(Measurement.prcp)).filter(Measurement.date > '2016-08-22').group_by(Measurement.date).all()
    return jsonify(Precipitation_last_year)

@app.route("/api/v1.0/stations")
def station():
    Station_stats = session.query(Station.station, Station.name).all()
    return jsonify(Station_stats)

@app.route("/api/v1.0/tobs") #NEED TO DO JUST THE TOP STATION!!!!!
def tobs():
    Top_station_data = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.date > '2016-08-22').all()
    return jsonify(Top_station_data)
    
@app.route("/api/v1.0/<start>") #getting error
def onlystartdate(date):
    
    start_temp_results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= date).all()
    return jsonify(start_temp_results)

@app.route("/api/v1.0/<start>/<end>") #getting null
def StartandEndDate(start,end):
    
    start_end_temp_results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(start_end_temp_results)


if __name__ == '__main__':
    app.run()