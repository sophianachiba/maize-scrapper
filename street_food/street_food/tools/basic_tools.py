def maize_api_search(maize_vendors, cur_vendor):
    maize_id = [vendor['id'] for vendor in maize_vendors
                if vendor['name'] == cur_vendor]

    if maize_id:
        return maize_id[0]
    else:
        return 'n/a'
