from flask import *
from modules.TinyDBController import TinyDBController
from modules.SeleniumController import SeleniumController
from modules.NetworkController import NetworkController

# For nginx server...
# app = Flask(__name__)

# For local server...
app = Flask(__name__, static_url_path='', static_folder='.',)

# GLOBAL VARIABLES
log_messages = [{'timestamp': '123 123', 'message': 'Hello world'}, {'timestamp': '124 124', 'message': 'Hello world again'}]

'''
# HOW TO USE TINYDBCONTROLLER:
TinyDBObj.tables['user'].purge_tables()
TinyDBObj.insert('user', {'name': 'a', 'age': 23})
TinyDBObj.insert('user', {'name': 'b', 'age': 23})
TinyDBObj.insert('user', {'name': 'c', 'age': 24})
print(TinyDBObj.tables['user'].all())
TinyDBObj.update('user', 'name', 'c', 'age', 99)
'''


def main():
    # start TinyDB process & load tables
    db = TinyDBController()
    db.load_tables(['user', 'logs'])

    # start selenium headless browser & login to Secomapp
    # selenium = SeleniumController()
    # selenium.start_browser()
    # selenium.secomapp_login()

    # run mlm network engine
    # mlm_network = NetworkController(db, selenium, 86400)


def create_error_response(message, code):
    payload = {"error_message": message, "http_code": code}
    return jsonify(payload), code


@app.route("/")
def homepage():
    title = "<h2>Sunfresh Referral Tracker is up and running!</h2>"
    status = "<p>Status: All good!</p>"
    header = "<div style='position: sticky; top: 0; background-color: white;'>{}{}</div>".format(title, status)
    log = ''
    for message in log_messages:
        log += '<li>{}: {}</li>'.format(message['timestamp'], message['message'])
    log = '<ul>{}</ul>'.format(log)
    # return header + log
    return header


@app.errorhandler(404)
def not_found(error):
    return "404 NOT FOUND!", 404


@app.errorhandler(405)
def method_not_allowed(error):
    return "405 METHOD NOT ALLOWED", 405


if __name__ == "__main__":
    main()
    app.run(port=5001)
