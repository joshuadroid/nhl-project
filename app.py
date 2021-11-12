import numpy as np
import psycopg2
import pandas as pd
import requests
import os

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template


#################################################
# Database Setup
#################################################
# Create the engine
# TODO Test and see if this works

# # From the config file
# from config import host_name, password, user_name
host_name = os.environ['host_name']
password = os.environ['password']
user_name = os.environ['user_name']

engine = psycopg2.connect(
    database="nhl_shots",
    user=user_name,
    password=password,
    host=host_name,
    port='5432'
)


app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgressql://{user_name}:{password}@ec2-34-200-161-87.compute-1.amazonaws.com:5432/nhl_shots"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# # reflect an existing database into a new model
# Base = automap_base()
# # # reflect the tables
# Base.prepare(engine, reflect=True)

# # # Save reference to the table
# NHL = Base.classes.nhl
# SHOTS = Base.classes.nhl_shots


#################################################
# Flask Routes
#################################################

@app.route("/index.html")
def home():
    return render_template("index.html")

@app.route("/Dashboard.html")
def dashboard():
    return render_template("Dashboard.html")

@app.route("/Data.html")
def data():
    return render_template("Data.html")


@app.route("/help")
def help():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/player/id<br/>"
        f"/api/v1.0/passengers"
    )




@app.route("/test")
def test_db():

    host_name = os.environ['host_name']
    password = os.environ['password']
    user_name = os.environ['user_name']

    engine = psycopg2.connect(
    database="nhl_shots",
    user=user_name,
    password=password,
    host=host_name,
    port='5432'
)
    
    df = pd.read_sql("SELECT * FROM shot_data LIMIT 5", engine)
    print(df)
    return df.to_json()

@app.route("/player/<id>")
def shots(id):

    host_name = os.environ['host_name']
    password = os.environ['password']
    user_name = os.environ['user_name']

    engine = psycopg2.connect(
    database="nhl",
    user=user_name,
    password=password,
    host=host_name,
    port='5432'
    )


    df = pd.read_sql(f"""SELECT * FROM "player_info" WHERE player_id = {id}""", engine)

    # # Create our session (link) from Python to the DB
    # session = Session(engine)

    # """Return a list of all passenger names"""
    # # Query all passengers
    # results = session.query(NHL.player_id == id).all()

    # session.close()

    # # Convert list of tuples into normal list
    # all_names = list(np.ravel(results))

    return df.to_json()


@app.route("/team/<id>")
def teams(id):

    host_name = os.environ['host_name']
    password = os.environ['password']
    user_name = os.environ['user_name']

    engine = psycopg2.connect(
    database="nhl",
    user=user_name,
    password=password,
    host=host_name,
    port='5432'
    )

    df = pd.read_sql(f"""SELECT * FROM "team_info" WHERE team_id = {id}""", engine)

    return df.to_json()

@app.route("/team/<id>/info")
def teams_info(id):

    host_name = os.environ['host_name']
    password = os.environ['password']
    user_name = os.environ['user_name']

    engine = psycopg2.connect(
    database="nhl",
    user=user_name,
    password=password,
    host=host_name,
    port='5432'
    )

    df = pd.read_sql(f"""SELECT * FROM "team_info" WHERE team_id = {id}""", engine)

    url = f"https://statsapi.web.nhl.com/api/v1/schedule?teamId={id}"
    response = requests.get(url)
    response_json = response.json()

    try:
        if response_json['dates'][0]:
            df['current_day_game'] = 'Game Tonight!'
    except IndexError:
        df['current_day_game'] = 'No Game Tonight'

    return df.to_json()








# @app.route("/api/v1.0/shots/player_id")
# def player_shots(player_id):
#     # Create the session
#     session = Session(engine)

#     # Query for all the shots from a player
#     results = session.query(SHOTS.player_id).\
#         filter_by("player_id" == player_id)
    
#     session.close()

#     return jsonify(results)


# @app.route("/api/v1.0/passengers")
# def passengers():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     """Return a list of passenger data including the name, age, and sex of each passenger"""
#     # Query all passengers
#     results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

#     session.close()

#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_passengers = []
#     for name, age, sex in results:
#         passenger_dict = {}
#         passenger_dict["name"] = name
#         passenger_dict["age"] = age
#         passenger_dict["sex"] = sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)


if __name__ == '__main__':
    app.run(debug=True)