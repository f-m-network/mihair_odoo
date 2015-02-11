# -*- coding: UTF-8 -*-
#
# Juan Hernandez, 2014
# @vladjanicek
# juan@qn.co.ve
#

import random


def get_random_hash():
    return str('%64x' % random.getrandbits(256))