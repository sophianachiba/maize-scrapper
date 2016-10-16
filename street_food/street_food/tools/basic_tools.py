from __future__ import division
from fuzzywuzzy import fuzz
import requests
from random import randrange
from decimal import Decimal, getcontext


def maize_api_search(maize_vendors, cur_vendor):
    maize_id = [vendor['id'] for vendor in maize_vendors
                if fuzz.ratio(vendor['name'], cur_vendor) > 80]

    if maize_id:
        return maize_id[0]
    else:
        return 'n/a'


def get_maize_vendors():
    url = "http://yumbli.herokuapp.com/api/v1/allkitchens/?format=json"
    maize_vendors = requests.get(url).json()

    return maize_vendors


def mix_location(location):
    getcontext().prec = 9

    rand_val = randrange(0, 100) / 1000000
    new_location = Decimal(location) + Decimal(rand_val)

    return str(new_location)
