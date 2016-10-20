# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import requests


class StreetFoodPipeline(object):
    def process_item(self, item, spider):
        return item


class ApiUploader(object):
    def __init__(self):
        self.api_url = "http://yumbli.herokuapp.com/api/v1/kitchenopentimes/"

    # EndPoint: http://yumbli.herokuapp.com/api/v1/kitchenopentimes/
    # PayLoad:
    # payload = {
    #   "kitchen": row[maize_id],
    #   "open_time": row[start_datetime],
    #   "close_time": row[end_datetime],
    #   "address": row[address],
    #   "latitude": row[latitude],
    #   "longitude": row[longitude],
    # }

    # for somastreetfood
    # sparkscocial
    # and off the grid

    def process_item(self, item, spider):
        if item['maize_id'] != 'n/a':
            data = {
                "kitchen": item['maize_id'],
                "open_time": item['start_datetime'],
                "close_time": item['end_datetime'],
                "address": item['address'],
                "latitude": item['latitude'],
                "longitude": item['longitude'],
            }
            # TODO: response is not handled.
            requests.post(self.api_url, data=data)

        return item
