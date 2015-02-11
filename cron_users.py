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

# Get Users
for user in get_api(api_url, 'users', token).json()['users']:
    print user

# Get User from Address API

# User exists?

#for prod in get_api(api_url, 'products', token).json()['products']:
