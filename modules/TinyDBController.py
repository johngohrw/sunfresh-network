from tinydb import TinyDB, Query
import datetime

# Guidelines for setting debug level:
# on global variable setting: 0 = include only important, 1 = include normal, 2 = include all
# on print statements: 0 = most important, 1 = normal, 2 = least important


class TinyDBController:
    def __init__(self, table_path='./tables', tables=None, debug=True, log=False):
        self.debug = debug
        self.debug_level = 1  # global debug variable. higher shows more detail.
        self.log = log
        self.tables = {}
        self.table_path = table_path
        for table in tables:
            self.load_table(table)
        self.debug_print("Controller initialized!")

    def debug_print(self, string, debug_level=0):
        prefix = "[TinyDB] "
        if self.log: self.insert('logs', {
            'timestamp': str(datetime.datetime.now()),
            'source': 'TinyDB',
            'text': string
        })
        if self.debug_level >= debug_level:
            if self.debug: print(prefix + string)

    def load_table(self, table_name):
        self.tables[table_name] = TinyDB(self.table_path + '/' + table_name + '.json')

    def insert(self, table_name, obj):
        self.tables[table_name].insert(obj)

    def update(self, table_name, query_key, query_value, update_key, update_value):
        q = Query()
        self.tables[table_name].update({update_key: update_value}, q[query_key] == query_value)
        # self.debug_print('updated {} to {} for {} == {} in table \'{}\''.format(update_key, update_value, query_key, query_value, table_name), 2)

    # returns a list
    def search(self, table_name, query_key, query_value):
        q = Query()
        return self.tables[table_name].search(q[query_key] == query_value)

    # only gets latest n entries from a table
    def get_latest(self, table_name, n):
        all_entries = self.tables[table_name].all()
        return all_entries[max(len(all_entries) - n, 0): len(all_entries)]
