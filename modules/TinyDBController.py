from tinydb import TinyDB, Query


class TinyDBController:
    def __init__(self, table_path='./tables', debug=True):
        print("[TinyDB] Controller initialized!")
        self.debug = debug
        self.tables = {}
        self.table_path = table_path

    def load_tables(self, tables):
        for table in tables:
            self.load_table(table)

    def load_table(self, table_name):
        if self.debug: print("[TinyDB] Loading from {}".format(table_name))
        self.tables[table_name] = TinyDB(self.table_path + '/' + table_name + '.json')
        if self.debug: print("[TinyDB] {} entries loaded".format(len(self.tables[table_name])))

    def insert(self, table_name, obj):
        self.tables[table_name].insert(obj)
        if self.debug: print('[TinyDB] inserted {} into table \'{}\''.format(obj, table_name))

    def update(self, table_name, query_key, query_value, update_key, update_value):
        q = Query()
        self.tables[table_name].update({update_key: update_value}, q[query_key] == query_value)
        if self.debug: print('[TinyDB] updated {} to {} for {} == {} in table \'{}\''.format(update_key, update_value, query_key, query_value, table_name))



