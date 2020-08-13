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

# @app.route("/")
# def welcome():


if __name__ == '__main__':
    app.run()