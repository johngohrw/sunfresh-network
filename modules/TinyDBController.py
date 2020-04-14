from tinydb import TinyDB, Query

# Guidelines for setting debug level:
# on global variable setting: 0 = include only important, 1 = include normal, 2 = include all
# on print statements: 0 = most important, 1 = normal, 2 = least important


class TinyDBController:
    def __init__(self, table_path='./tables', debug=True):
        self.debug = debug
        self.debug_level = 1  # global debug variable. higher shows more detail.
        self.debug_print("Controller initialized!")
        self.tables = {}
        self.table_path = table_path

    def debug_print(self, string, debug_level=0):
        prefix = "[TinyDB] "
        if self.debug_level >= debug_level:
            if self.debug: print(prefix + string)

    def load_tables(self, tables):
        for table in tables:
            self.load_table(table)

    def load_table(self, table_name):
        self.debug_print("Loading from {}".format(table_name), 1)
        self.tables[table_name] = TinyDB(self.table_path + '/' + table_name + '.json')
        self.debug_print("{} entries loaded".format(len(self.tables[table_name])), 1)

    def insert(self, table_name, obj):
        self.tables[table_name].insert(obj)
        self.debug_print('inserted {} into table \'{}\''.format(obj, table_name), 2)

    def update(self, table_name, query_key, query_value, update_key, update_value):
        q = Query()
        self.tables[table_name].update({update_key: update_value}, q[query_key] == query_value)
        self.debug_print('updated {} to {} for {} == {} in table \'{}\''.format(update_key, update_value, query_key, query_value, table_name), 2)

    # returns a list
    def search(self, table_name, query_key, query_value):
        q = Query()
        return self.tables[table_name].search(q[query_key] == query_value)

