import datetime
import csv

csv_columns = 'order_name,customer_email,purchased_item,purchased_item_price,purchased_item_quantity,' \
              'purchased_item_subtotal,referrer_id,referrer_email,commission_product_rule,commission_percentage,' \
              'referrer_commission_amount'

class OrderController:
    def __init__(self, db_engine, mlm_network, referral_bonus_rules):
        self.db_engine = db_engine
        self.mlm_network = mlm_network
        self.referral_bonus_rules = referral_bonus_rules
        self.payment_list = []
        self.debug = True
        self.log = True

    def debug_print(self, string):
        prefix = "[OrderController] "
        if self.log: self.db_engine.insert('logs', {
            'timestamp': str(datetime.datetime.now()),
            'source': 'OrderController',
            'text': string
        })
        if self.debug: print(prefix + string)

    def read_csv(self, filepath):
        self.payment_list = []

        with open(filepath, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            item_list = []
            previous_order = ''
            previous_email = ''
            for line in csv_reader:
                current_order = line['Name']
                current_email = line['Email']
                # its a new order!
                if current_order != previous_order:
                    # process previous order
                    if len(item_list) > 0:
                        self.process_order(previous_email, previous_order, item_list)
                    item_list = []
                item_list.append({
                    'name': line['Lineitem name'],
                    'quantity': line['Lineitem quantity'],
                    'price': line['Lineitem price']
                })
                previous_order = current_order
                previous_email = current_email
            self.process_order(previous_email, previous_order, item_list)
        self.debug_print('Processed {} payable bonus payments'.format(len(self.payment_list)))

    def process_order(self, email, order_id, item_list):
        # if this order does not exist in the history already
        if not self.db_engine.exists('order_history', 'order_id', order_id):
            self.db_engine.insert('order_history', {'order_id': order_id})
            user_id = self.mlm_network.get_user_id_by_email(email)
            # if email exists in secomapp
            if user_id != 0:
                # for each item
                for item in item_list:
                    rule_applied = False
                    for rule in self.referral_bonus_rules:
                        if rule['product_name'] == item['name']:  # product rule match!
                            item_subtotal = int(item['quantity']) * float(item['price'])
                            bonus_payments = self.mlm_network.get_bonus_payments(user_id, item_subtotal, rule['bonus_tiers'])
                            self.process_bonus_payments(
                                order_id, email, bonus_payments, item['name'], item['price'],
                                item['quantity'], item_subtotal, rule['product_name']
                            )
                            rule_applied = True
                            break
                    if not rule_applied:
                        item_subtotal = int(item['quantity']) * float(item['price'])
                        bonus_payments = self.mlm_network.get_bonus_payments(user_id, item_subtotal, self.referral_bonus_rules[0]['bonus_tiers'])
                        self.process_bonus_payments(
                            order_id, email, bonus_payments, item['name'], item['price'],
                            item['quantity'], item_subtotal, self.referral_bonus_rules[0]['product_name']
                        )

    def process_bonus_payments(self, order_id, customer_email, bonus_payments, purchased_item,
                               purchased_item_price, purchased_item_quantity, purchased_item_subtotal,
                               commission_product_rule):
        for payment in bonus_payments:
            bonus_payment_string = '{},{},{},{},{},{},{},{},{},{},{}'.format(
                order_id, customer_email, purchased_item, purchased_item_price, purchased_item_quantity,
                purchased_item_subtotal, payment['id'], self.mlm_network.get_email_by_id(payment['id']),
                commission_product_rule, payment['commission_percentage'], payment['payment']
            )
            self.payment_list.append(bonus_payment_string)

    def get_latest_csv(self):
        csv_file = csv_columns + '\n'
        for payment_string in self.payment_list:
            csv_file += payment_string + '\n'
        return csv_file
