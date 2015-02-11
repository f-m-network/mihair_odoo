# -*- coding: utf-8 -*-
#
# Juan Hernandez, 2014
# juan@qn.co.ve
# @vladjanicek
#

import os
from raven import Client


# Set Sentry
sentry_id = os.environ.get('SENTRY_ID')
client = Client('https://{}@app.getsentry.com/29489'.format(sentry_id))


def mihair_customer(customer, odoolib):
    """Adds customer. Returns partner ID.

    get or create customer

    :param customer: spree customer dictionary

    """

    partner = {
        'name': customer.get('name', ''),
        'email': customer.get('email', ''),
        'company_id': 1,
        'active': True,
        'customer': True,
        'supplier': False,
        # Set ACC
    }

    # TODO: Upgrade code with new get_or_create method in odoolib
    try:
        return odoolib.res_partner.add(partner)
    except Exception, e:
        # Return Partner ID in case it exists
        return odoolib.res_partner.get(email=customer.get('email')).get('id')
