"""
Package: service
Package for the application models and service routes
This module creates and configures the Flask app and sets up the logging
and SQL database
"""
import sys
from flask import Flask
from service import config
from service.common import log_handlers
from flask_talisman import Talisman
from flask_cors import CORS  # Import CORS

# Create Flask application
app = Flask(__name__)
app.config.from_object(config)

# Initialize Talisman for security headers
talisman = Talisman(app)

# Initialize CORS
CORS(app)  # Add this line to enable CORS

# Import the routes after the Flask app is created
from service import routes, models  # noqa: F401 E402

# Pylint disable for cyclic-import and wrong-import-position
from service.common import error_handlers, cli_commands  # noqa: F401 E402

# Set up logging for production
log_handlers.init_logging(app, "gunicorn.error")

app.logger.info(70 * "*")
app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")

try:
    models.init_db(app)  # Make our database tables
except Exception as error:  # Pylint disable broad-except
    app.logger.critical("%s: Cannot continue", error)
    sys.exit(4)

app.logger.info("Service initialized!")
