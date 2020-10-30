from flask import Flask

app = Flask(__name__)

from worldbank2 import routes
