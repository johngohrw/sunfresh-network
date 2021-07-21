from flask import *
from modules.TinyDBController import TinyDBController
from modules.SeleniumController import SeleniumController
from modules.NetworkController import NetworkController
from modules.OrderController import OrderController
from werkzeug.utils import secure_filename
import os
import numpy as np
import csv

referral_bonus_rules = [
    {'product_name': 'default', 'bonus_tiers': [0.05]},  # applies to all products
    {'product_name': '*Member Signup Package 1', 'bonus_tiers': [0.08, 0.02, 0.02]},
    {'product_name': '*Member Signup Package 2', 'bonus_tiers': [0.16, 0.04, 0.04]},
    {'product_name': 'Member Signup Package 1', 'bonus_tiers': [0.08, 0.02, 0.02]},
    {'product_name': 'Member Signup Package 2', 'bonus_tiers': [0.16, 0.04, 0.04]},
]

# For nginx server...
app = Flask(__name__)

# For local server...
# app = Flask(__name__, static_url_path='', static_folder='.',)


'''
# HOW TO USE TINYDBCONTROLLER:
TinyDBObj.tables['user'].purge_tables()
TinyDBObj.insert('user', {'name': 'a', 'age': 23})
TinyDBObj.insert('user', {'name': 'b', 'age': 23})
TinyDBObj.insert('user', {'name': 'c', 'age': 24})
print(TinyDBObj.tables['user'].all())
TinyDBObj.update('user', 'name', 'c', 'age', 99)
'''


# start TinyDB process & load tables
db_engine = TinyDBController('./tables',['user', 'logs', 'rules', 'order_history'], True, True)

# start selenium headless browser
selenium = SeleniumController(True, db_engine)

# run mlm network engine
mlm_network = NetworkController(db_engine, selenium, 86400, True)

# run Order Controller
order_engine = OrderController(db_engine, mlm_network, referral_bonus_rules)


def create_error_response(message, code):
    payload = {"error_message": message, "http_code": code}
    return jsonify(payload), code


@app.route("/")
def homepage():
    title = "<h2>Sunfresh Referral Tracker is up and running!</h2>"
    status = "<p>Status: All good!</p>"
    header = "<div style='position: sticky; top: 7px; " \
             "background-color: #1474ab; padding: 10px 30px; " \
             "color: white;'>{}{}</div>".format(title, status)
    latest_logs = db_engine.get_latest('logs', 50)
    latest_logs.reverse()
    logs = ''
    for log_entry in latest_logs:
        logs += '<li style="margin-bottom: 10px;">' \
                '<div class="message-header" style="color: #222">' \
                '<span class="source" style="margin-right: 15px">[{}]</span>' \
                '<span class="timestamp">{}</span>' \
                '</div>' \
                '<span class="text" style="color: #000">' \
                '{}' \
                '</span>' \
                '</li>'.format(log_entry['source'], log_entry['timestamp'], log_entry['text'])
    logs = '<ul>{}</ul>'.format(logs)
    return header + logs


app.config["ALLOWED_EXTENSIONS"] = {'csv'}


def valid_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config["ALLOWED_EXTENSIONS"]


def handle_csv_upload(request):
    # check if the post request has the file part
    if 'file' not in request.files:
        print('No file part')
        return
    file = request.files['file']

    # save csv locally
    file.save(os.path.join('./uploads', secure_filename(file.filename)))

    # reads csv file with csv reader
    order_engine.read_csv('./uploads/' + file.filename)


@app.route('/upload-csv', methods=['POST'])
def csv_upload_endpoint():
    handle_csv_upload(request)
    payload = {"results": 'lol'}
    response = jsonify(payload)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200


@app.route('/rebuild-network', methods=['POST'])
def rebuild_network():
    selenium.start_browser()
    selenium.secomapp_login()
    mlm_network.build_network()
    selenium.close_browser()
    payload = {"status": 'success'}
    response = jsonify(payload)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200


@app.route('/logs', methods=['GET'])
def logs_endpoint():
    latest_logs = db_engine.get_latest('logs', 300)
    payload = {"logs": latest_logs}
    response = jsonify(payload)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200


@app.route("/get-latest-csv")
def get_latest_csv():
    csv_file = order_engine.get_latest_csv()
    return Response(
        csv_file,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=latest_bonus_payments.csv"})


@app.errorhandler(404)
def not_found(error):
    return "404 NOT FOUND!", 404


@app.errorhandler(405)
def method_not_allowed(error):
    return "405 METHOD NOT ALLOWED", 405


if __name__ == "__main__":
    app.run(port=5060)
