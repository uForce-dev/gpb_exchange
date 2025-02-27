from flask import Flask, request

app = Flask(__name__)

@app.route('/gpb/check-avail')
def check_avail():
    return 'check_avail'

@app.route('/gpb/payment-reg')
def payment_reg():
    return 'payment_reg'

if __name__ == '__main__':
    app.run()