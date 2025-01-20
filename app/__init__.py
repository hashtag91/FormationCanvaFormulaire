from flask import Flask
import sqlite3

# Initialisation de Flask
app = Flask(__name__)

# Chargement des routes

from app import routes
