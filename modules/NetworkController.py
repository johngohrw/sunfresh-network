import time
import datetime
from timeit import default_timer as timer

'''
TinyDBController table structure

user object:
{
    'id': Number,
    'first_name': String,
    'last_name': String,
    'parent_id': Number,
    'children': id[],
    'email': String
}
'''


class NetworkController:
    def __init__(self, db_controller, selenium_controller, process_interval_seconds):
        self.process_interval = process_interval_seconds
        self.running = True
        self.debug = True
        self.debug_print("Network Controller initialized!")

        # getting running Selenium and TinyDB controller instances
        self.selenium = selenium_controller
        self.db = db_controller

        # main process lifecycle
        while self.running:
            self.process()

        # terminate lifecycle
        self.debug_print("Network Controller process terminated.")
        self.selenium.close_browser()

    def process(self):
        start_time = timer()
        self.debug_print("Starting process cycle")
        if self.selenium.browser_is_running():  # if selenium browser is running
            # Process cycle start ===========================

            self.build_network()  # build network from scratch

            # Process cycle end =============================
        else:
            self.debug_print("Selenium browser is not running! Process cycle skipped.")
        end_time = timer()
        duration = end_time - start_time
        delay = self.process_interval - duration
        self.debug_print("Process cycle took {:7.2f} seconds. "
                         "Starting next process cycle in {:7.2f} seconds".format(duration, delay))
        time.sleep(delay)

    def quit_process(self):
        self.debug_print("quitting process after current running iteration..")
        self.running = False

    def debug_print(self, string):
        prefix = "[NetworkCtrl] {} - ".format(datetime.datetime.now())
        if self.debug: print(prefix + string)

    # builds user network from scratch. requires login
    def build_network(self):
        self.debug_print("Building network..")
        self.db.tables['user'].purge_tables()  # clears all entries in table
        all_users = self.get_all_users()
        for user in all_users:
            user_info = self.get_user_info(user['id'])
            self.db.insert('user', {
                'id': user['id'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'email': user['email'],
                'parent_id': user_info['parent_id'],
                'children': [],
            })
        self.debug_print("Users fetched, connecting parent and child nodes")
        for user in all_users:
            user_id = user['id']
            # get current user's parent id from local db
            user_db_obj = self.db.search('user', 'id', user_id)[0]
            parent_id = user_db_obj['parent_id']
            # if this user has a parent
            if parent_id > 0:
                # append this user's id to its parent's children list
                parent_object = self.db.search('user', 'parent_id', parent_id)[0]
                children_list = parent_object['children']
                children_list.append(user['id'])
                self.db.update('user', 'id', parent_id, 'children', children_list)
                self.debug_print('Linked  {} --> {}'.format(user_id, parent_id))
        self.debug_print("Build network complete!")

    # fetches from secomapp the user's details. requires login.
    def get_user_info(self, user_id):
        payload = self.selenium.fetch_json('https://af.secomapp.com/admin/affiliates/{}'.format(user_id))
        return payload['data']

    # fetches from secomapp a list of all users. requires login.
    def get_all_users(self):
        payload = self.selenium.fetch_json('https://af.secomapp.com/admin/affiliates/datatables')
        return payload['data']

    # given an id, get its parent_id from local db
    def get_parent(self, user_id):
        user_object = self.db.search('user', 'id', user_id)[0]
        return user_object['parent_id']

    # get a list of bonus payments towards parent referrers from
    # a particular product purchased by its children
    def get_bonus_payments(self, user_id, product_amount, bonus_list):
        # example bonus list (8%, 2%, 2%) = [0.08, 0.02, 0.02]
        current_id = user_id
        payments = []
        for i in range(bonus_list):
            current_user_obj = self.db.search('user', 'id', current_id)[0]
            # this user has a parent
            if current_user_obj['parent_id'] > 0:
                current_id = current_user_obj['parent_id']  # select the parent
                payment_amount = bonus_list[i] * product_amount
                payments.append({'id': current_id, 'payment': payment_amount})  # Add a payment
            # if this user has no parent, quit the loop
            else:
                break
        return payments


if __name__ == "__main__":
    pass
