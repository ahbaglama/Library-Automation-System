from flask import Blueprint, jsonify

home_blueprint = Blueprint('home', __name__)

@home_blueprint.route('/home')

def home():
    return 'Welcome to the home page!'