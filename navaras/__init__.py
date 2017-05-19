"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)
#app.debug = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super_secret_key_230742'

import navaras.views
