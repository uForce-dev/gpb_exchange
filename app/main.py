import logging

from flask import Flask

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("../logs/app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/gpb/check-avail')
def check_avail():
    logger.info("Received request on /gpb/check-avail")
    return 'check_avail'


@app.route('/gpb/payment-reg')
def payment_reg():
    logger.info("Received request on /gpb/payment-reg")
    return 'payment_reg'


if __name__ == '__main__':
    logger.info("Starting Flask app...")
    app.run()
