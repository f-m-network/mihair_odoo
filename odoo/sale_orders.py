# -*- coding: UTF-8 -*-
#
# Juan Hernandez, 2014
# @vladjanicek
# juan@qn.co.ve
#

import os
from raven import Client

# Set Sentry
sentry_id = os.environ.get('SENTRY_ID')
client = Client('https://{}@app.getsentry.com/29489'.format(sentry_id))


def create_so(partner, spree_order_number, odoolib):
    partner_info = {
        'name': "SPREE {}".format(spree_order_number),
        'partner_id': partner.get('id'),
        'spree_order_id': spree_order_number,

        # Using 1 as basic since pricelists are not being used
        'pricelist_id': 1,
        'partner_invoice_id': partner.get('id'),
        'partner_shipping_id': partner.get('id')
    }
    return odoolib.sale_order.add(partner_info)


def add_line_so(sale_order_id, product, qty, odoolib):
    sale_order_records = {
        'order_id': sale_order_id,
        'product_id': product.get('id'),
        #'product_uom': product.get('uom_po_id')[0],
        'product_uom_qty': qty,
        #'tax_id': [(6, 0, p.get('taxes_id'))],
        'price_unit': product.get('list_price'),
        'name': product.get('partner_ref')
    }
    return odoolib.sale_order_line.add(sale_order_records)



#def add_po(pv, bill, ship, odoolib):
#    po_records = {
#        # Supplier
#        'partner_id': pv.get('vendor_id'),
#
#        # oerp does not handle payments for mihair
#        'invoice_method': 'manual',
#
#        # Check values
#        'location_id': 1,
#        'pricelist_id': 1,
#        'currency_id': 1,
#        'company_ud': 1,
#
#        # Spree
#        'spree_order_id': pv.get('spree_order_id'),
#        #'spree_order_line_id': pv.get('spree_order_line_id'),
#
#        # Billing Address
#        'spree_billing_full_name': bill.get('full_name', ''),
#        'spree_billing_address1': bill.get('address1', ''),
#        'spree_billing_address2': bill.get('address2', ''),
#        'spree_billing_city': bill.get('city', ''),
#        'spree_billing_state': bill.get('state_text', ''),
#        'spree_billing_zip': bill.get('zipcode', ''),
#        'spree_billing_phone': bill.get('phone', ''),
#
#        # Shipping Address
#        'spree_shipping_full_name': ship.get('full_name', ''),
#        'spree_shipping_address1': ship.get('address1', ''),
#        'spree_shipping_address2': ship.get('address2', ''),
#        'spree_shipping_city': ship.get('city', ''),
#        'spree_shipping_state': ship.get('state_text', ''),
#        'spree_shipping_zip': ship.get('zipcode', ''),
#        'spree_shipping_phone': ship.get('phone', ''),
#    }
#
#    # Create PO
#    po = odoolib.purchase_order.add(**po_records)
#    # Add order lines to purchase orders
#    for line in pv.get('spree_order_line_id'):
#        odoolib.purchase_order_spree.add({'po_id': po,
#                                          'spree_order_line': line})
#    return po
#
#
#def add_line_po(po_id, product, qty, odoolib):
#    records = {
#        'order_id': po_id,
#        'product_id': product.get('id', ''),
#        # TODO: test defaults
#        #'product_uom': product.get('uom_po_id', '')[0],
#        # Set 1 for unit
#        'product_uom': 1,
#        'product_qty': qty,
#        # TODO: check taxes
#        'tax_id': [(6, 0, product.get('taxes_id'))],
#        'price_unit': product.get('list_price'),
#        'name': product.get('partner_ref'),
#        # TODO: Set testing date for tomorrow
#        'date_planned': '2014-08-22',
#    }
#
#    return odoolib.purchase_order_line.add(records)
#
