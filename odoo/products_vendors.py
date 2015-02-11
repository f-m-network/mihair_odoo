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


##
# Product/Vendor spree sync
def add_product(prod, odoolib):
    product = {
        # TODO: Check categories
        'categ_id': 1,
        'mihair_product_id': prod.get('id', ''),
        'name': prod.get('name', ''),
        'description': prod.get('description', ''),
        'list_price': prod.get('price', ''),
        'default_code': prod.get('sku', ''),
        'active': True,
        'purchase_ok': True,
        'sale_ok': True,
        'type': 'service',
        'procure_method': 'make_to_order',
        'supply_method': 'buy',
    }
    try:
        return odoolib.product_product.add(product)
    except Exception, e:
        client.captureException()


def mihair_vendor(vendor, odoolib):
    """Adds partner. Returns partner ID.

    Adds partner, if not, will hit the database for its record id

    :param vendor: spree vendor dictionary

    """
    partner = {
        'mihair_vendorid': vendor.get('id'),
        'name': vendor.get('company', ''),
        #'email': vendor.get('email', ''),
        'company_id': 1,
        'active': True,
        'customer': False,
        'supplier': True,
        #'phone': telephone,
        #'property_account_payable': property_account_payable,
        #'property_account_receivable': property_account_receivable
    }

    # TODO: Upgrade code with new get_or_create method in odoolib
    try:
        return odoolib.res_partner.add(partner)
    except Exception, e:
        return odoolib.res_partner.get(
            mihair_vendorid=vendor.get('id')).get('id')


def relate_vendor_product(product_id, partner_id, odoolib):
    print partner_id
    vendor_dict = {
        'company_id': 1,
        'product_id': product_id,
        # (vendor_id)
        'name': partner_id,
        'min_qty': 0,
        'qty': 0,
    }
    try:
        return odoolib.product_supplierinfo.add(vendor_dict)
    except Exception, e:
        client.captureException()
