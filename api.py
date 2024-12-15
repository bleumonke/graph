from flask import Flask
from routes import health, chat
import logging, logging.config, yaml

with open('logging.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

app = Flask(__name__)
logger.info('Starting the application')
app.register_blueprint(health, url_prefix='/health')
app.register_blueprint(chat, url_prefix='/chat')
app.run(debug=True, host='0.0.0.0', port=5000)