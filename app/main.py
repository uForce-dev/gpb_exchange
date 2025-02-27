import logging
from flask import Flask, request

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

@app.route('/gpb/check-avail', methods=['GET', 'POST'])
def check_avail():
    logger.info("Received request on /gpb/check-avail")
    logger.info("Request data: %s", request.data)
    logger.info("Request args: %s", request.args)
    logger.info("Request form: %s", request.form)
    return 'check_avail'

@app.route('/gpb/payment-reg', methods=['GET', 'POST'])
def payment_reg():
    logger.info("Received request on /gpb/payment-reg")
    logger.info("Request data: %s", request.data)
    logger.info("Request args: %s", request.args)
    logger.info("Request form: %s", request.form)
    return 'payment_reg'

if __name__ == '__main__':
    logger.info("Starting Flask app...")
    app.run()
