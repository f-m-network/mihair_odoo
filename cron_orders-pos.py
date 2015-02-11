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
        # Get order line loop... using record_id for testing
        spree_order = get_api(API_URL, 'orders',
                              TOKEN, record_id=order.get('number'))
        prod_vendors = []
        qty = 0
        # Get order lines
        for line in spree_order.json().get('line_items'):
            # Spree Product ID
            variant_id = line.get('variant_id', ''),
            qty = line.get('quantity', ''),

            # oerp product
            odoo_product = ol.product_product.get(
                mihair_product_id=variant_id[0],
                model_fields=['mihair_product_id']
            )

            # Make sure the order line is not already processed in Odoo
            #if ol.purchase_order.get(spree_order_line_id=line.get('id')):
            if ol.purchase_order_spree.get(spree_order_line=line.get('id')):
                print ('Order {} Line {} has already been'
                       ' processed'.format(order.get('number'),
                                           line.get('id')))
            else:
                print 'Procesing Order {} line {}'.format(order.get('number'),
                                                          line.get('id'))
                # Get product vendor ## keep PEP 8
                opd = odoo_product.get('id')
                vendor = ol.product_supplierinfo.get(product_id=opd)

                # Add vendor to prod_vendors list if they don't exist already
                v = vendor.get('name')[0],
                if v[0] not in [pd.get('vendor_id') for pd in prod_vendors]:
                    prod_vendors.append({
                        'vendor_id': vendor.get('name')[0],
                        # [prod, qty]
                        'prods': [],
                        'spree_order_id': order.get('number'),
                        'spree_order_line_id': []
                    })

                # Group product vendor
                for vn in prod_vendors:
                    if vn.get('vendor_id') == vendor.get('name')[0]:
                        vn['prods'].append([odoo_product.get('id'), qty[0]])
                        vn['spree_order_line_id'].append(line.get('id'))
        #if prod_vendors:
        #    print prod_vendors

        # Create purchase orders, one for each vendor
        for pv in prod_vendors:
            # Current addresses
            bill = spree_order.json().get('bill_address')
            ship = spree_order.json().get('ship_address')

            # Create PO
            purchase_order_id = po.add_po(pv, bill, ship, ol)

            # Add products to PO
            for prod_id in pv.get('prods'):
                product = ol.product_product.get(id=prod_id[0],
                                                 model_fields=[
                                                     'name',
                                                     'spree_product_id',
                                                     'taxes_id',
                                                     'list_price',
                                                     'partner_ref'])

                order_line_id = po.add_line_po(purchase_order_id,
                                               product, prod_id[1], ol)

            # Confirm Purchase Order
            ol.purchase_order.exec_workflow('purchase_confirm',
                                            purchase_order_id)

            print ('Odoo PO {} has been created for '
                   'order {}'.format(purchase_order_id, order.get('number')))
            ##
            # Send PO to vendor
            random_url = get_random_hash()
            msg = ('A new Purchase Order has been created. Please follow this '
                   '<a href="http://{}/po/{}">here</a> to '
                   'access PO: {}'.format(MIHAIR_CHERRYPY_URL,
                                          random_url, purchase_order_id))

            # Add Random number to PO
            ol.purchase_order.update(purchase_order_id, cherrypy_id=random_url)
            pdf_file = ol.purchase_order.get_report(
                'purchase.order',
                purchase_order_id,
                '{}/pdfs/po_{}.pdf'.format(MIHAIR_CHERRYPY_PATH,
                                           purchase_order_id)
            )

            # TODO: get email addresses from vendor info
            # TODO: check when to confirm PO
            send_html_message(
                ['vladjanicek@gmail.com', 'juan@qn.co.ve'],
                'New Purchase Order from mi.Hair', msg,
                files='{}/pdfs/po_{}.pdf'.format(MIHAIR_CHERRYPY_PATH,
                                                 purchase_order_id)
            )
