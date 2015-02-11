import unittest
import types

from odoolib.api import OdooLib

#
# Warning: Use TEST DB as it will create a lot of records
#


class TestProductVendors(unittest.TestCase):

    def setUp(self):
        # Todo: Get from testdata
        self.ol = OdooLib('http://dev:8069', 'fmn', 'admin', 'admin')
        self.prod = {
            'mihair_productid': 123,
            'name': 'miHair Product 123',
            'description': 'This is my Product Description',
            'list_price': 123.12,
            'default_code': 'SKU123123'
        }

    def test_add_product(self):
        """Add product into Odoo """
        self.prod_id = self.ol.product_product.add(self.prod),
        self.assertIsInstance(self.prod_id[0], types.IntType)

    def test_repeated_product(self):
        # Get SKU from DB
        #default_code = self.prod.get('default_code')
        #r = self.ol.product_product.get(default_code=default_code)
        pass


if __name__ == '__main__':
    unittest.main()
