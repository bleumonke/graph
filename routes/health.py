from flask import Blueprint, jsonify
import logging

health = Blueprint('health', __name__)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.propagate = False

@health.route('/', methods=['GET'])
def health_check():
    logger.info('Health check successful')
    return jsonify({'message': 'Healthy!'}), 200


# LISTCALLS
# OVERWIWCALL
# / -> snapshot
# /summary -> summary
# /adherence -> adherence
# /segment -> segment
# /transcript -> transcript
# /download -> download