import csv
from urllib2 import urlopen
import urllib
import urllib2

f = open('offthegrid-data.csv')
csv_f = csv.reader(f)

header = next(csv_f)
maize_status = header.index('maize_status')
start_datetime = header.index('start_datetime')
longitude = header.index('longitude')
end_datetime = header.index('end_datetime')
address = header.index('address')
latitude = header.index('latitude')
maize_id = header.index('maize_id')
VendorName = header.index('VendorName')

payload = {}
url = 'http://yumbli.herokuapp.com/api/v1/kitchenopentimes/'
total = 0
uploaded = 0
for row in csv_f:
	total +=1
	if row[maize_status] == 'found':
		payload = {
			"kitchen": row[maize_id],
			"open_time": row[start_datetime],
			"close_time": row[end_datetime],
			"address": row[address],
			"latitude": row[latitude],
			"longitude": row[longitude],
		}
		print 'sending request...'
		print payload
		data = urllib.urlencode(payload)
		request = urllib2.Request(url, data)
		response = urllib2.urlopen(request)
		print 'response:'
		html = response.read()
		uploaded +=1
		print html
		
print "total entries: " + str(total) + " / uploaded entries: " +  str(uploaded)
