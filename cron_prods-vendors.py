# -*- coding: UTF-8 -*-
#
# Juan Hernandez, 2014
# @vladjanicek
# juan@qn.co.ve
#

import os

from odoolib.api import OdooLib

from lib.rqst import get_api

import odoo.products_vendors as pd


api_url = os.environ.get('API_URL')
token = os.environ.get('TOKEN')

# Odoo Credentials
ODOO_URL = os.environ.get('ODOO_URL')
ODOO_DB = os.environ.get('ODOO_DB')
ODOO_USER = os.environ.get('ODOO_USER')
ODOO_PASSWORD = os.environ.get('ODOO_PASSWORD')

ol = OdooLib(ODOO_URL, ODOO_DB, ODOO_USER, ODOO_PASSWORD)


for prod in get_api(api_url, 'products', token).json()['products']:

    # Check if product exists:

        # Add master product info
        master_id = prod.get('master').get('id')
        product = ol.product_product.get(mihair_product_id=master_id,
                                         model_fields=['mihair_product_id'])
        if not product:
            product_id = pd.add_product(prod.get('master'), ol)
        else:
            product_id = product.get('id')
            print '{} is already in the DB'.format(prod.get('id'))

        # Vendor info
        vendor_id = prod.get('master').get('vendor_id')
        vendor = get_api(api_url, 'vendors', token, vendor_id).json()
        vendor_id = pd.mihair_vendor(vendor, ol)

        if not product:
            # Product-Supplier
            print 'Vendor ID: ', vendor_id
            print 'Setting Prod-Vendor Relationship'
            print pd.relate_vendor_product(product_id, vendor_id, ol)

        # Add variants if they exist
        if prod.get('has_variants'):
            for variant in prod.get('variants'):
                print 'Variant Product'
                v_pr = ol.product_product.get(id=variant.get('id'))
                if not v_pr:
                    product_id = pd.add_product(variant, ol)
                    # Product-Supplier
                    pd.relate_vendor_product(product_id, vendor_id, ol)
                    print 'Vendor-Variant'
                else:
                    print 'VPR: ', v_pr
                    print 'Product Variant already in DB'
