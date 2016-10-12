from fuzzywuzzy import fuzz
import requests


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
