# -*- coding: UTF-8 -*-
#
# Juan Hernandez, 2014
# @vladjanicek
# juan@qn.co.ve
#

# TODO: filter orders by day
#

import os

from lib.rqst import get_api
from lib.mailgun import send_html_message
from lib.hashes import get_random_hash

from odoolib.api import OdooLib

import odoo.products_vendors as pd
import odoo.purchase_orders as po
import odoo.customers as cus
import odoo.sale_orders as so

# Script Constants
API_URL = os.environ.get('API_URL')
TOKEN = os.environ.get('TOKEN')
MIHAIR_CHERRYPY_URL = os.environ.get('MIHAIR_CHERRYPY_URL')
MIHAIR_CHERRYPY_PATH = os.environ.get('MIHAIR_CHERRYPY_PATH')

# Odoo Credentials
ODOO_URL = os.environ.get('ODOO_URL')
ODOO_DB = os.environ.get('ODOO_DB')
ODOO_USER = os.environ.get('ODOO_USER')
ODOO_PASSWORD = os.environ.get('ODOO_PASSWORD')

ol = OdooLib(ODOO_URL, ODOO_DB, ODOO_USER, ODOO_PASSWORD)

##
# Populate Purchase Order
#
# Get all orders
for order in get_api(API_URL, 'orders', TOKEN).json().get('orders'):
    if order.get('payment_state') == 'paid':

        print 'Order {}'.format(order.get('number'))
        # Check if order had already been processed
        if ol.sale_order.get(spree_order_id=order.get('number')):
            print 'Order {} already processed'.format(order.get('number'))
        else:

            # Get single order for current object
            spree_order = get_api(API_URL, 'orders',
                                  TOKEN, record_id=order.get('number')).json()

            # Get user login
            user_email = order.get('email')
            print user_email

            # Get User Information from Address and use user login as email
            # for the customer partner profile (Use billing address as it is
            # the default address)
            bill = spree_order.get('bill_address')
            ship = spree_order.get('ship_address')

            ## Create User Object
            customer = {
                'email': user_email,
                'name': bill.get('full_name')
            }
            ## Get/Set its Odoo ID
            customer['id'] = cus.mihair_customer(customer, ol)

            # Get into Order Lines
            prod_vendors = []
            qty = 0
            # Create Sale order (Set mode where every PO is
            # created once approved)
            print 'creating SO ',
            sale_order_id = so.create_so(customer,
                                         spree_order.get('number'),
                                         ol)
            print sale_order_id

            for line in spree_order.get('line_items'):
                # Spree Product ID
                variant_id = line.get('variant_id', ''),
                qty = line.get('quantity', ''),

                # oerp product
                odoo_product = ol.product_product.get(
                    mihair_product_id=variant_id[0]
                )

                # Make sure the order line is not already processed in Odoo
                line_id = line.get('id')

                # Add order lines to current order
                print 'Adding line ',
                print so.add_line_so(sale_order_id, odoo_product, qty[0], ol)

            # Confirm Sale Order
            print "...Confirming Order ", sale_order_id
            ol.sale_order.exec_workflow('order_confirm', sale_order_id)
            print "...Creating Draft Invoice"
            ol.sale_order.exec_workflow('manual_invoice', sale_order_id)


            # Process payment in its own account for GL

            # Search for newly created POs

            # Send POs to Vendor

