from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_scrape
import os


app = Flask(__name__)   