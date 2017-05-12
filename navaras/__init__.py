"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)
#app.debug = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

import navaras.views
