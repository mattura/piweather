# Run this in a cron every minute (MetData<3.4/m, OpenLDBWS<2/s)
# log output to a file for errors
# This technique eliminates delays during the fetch phase
# make sure to "pip install nre-darwin-py" and use python 2 only
import os,sys
import time, urllib2,json
from nredarwin.webservice import DarwinLdbSession

#Get Met office weather for all data locations specified in met.conf
#and write them to a file #####.dat
try:
	with open(os.path.join(sys.path[0], 'met.conf'), 'rb') as f:
		d = eval(f.read())
	apikey = d['apikey']
	loc = d['locations']
except:
	print "Invalid configuration file"
for l in loc:
	try:
		url="http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/"+str(l)+"?res=3hourly&key="+apikey
		data=urllib2.urlopen(url)
		with open(os.path.join(sys.path[0], '_'+str(l)+'.dat'), 'w') as g:
			g.write(data.read())
	except:
		print "%s - Error fetching data for location %s " % (time.strftime("%Y-%m-%d %H:%I:%S"), str(l))

#Get National Rail data for route specified in nre.conf
#and write to file
#wsdlu = "https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx" #plus date
wsdlu = "https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2016-02-16"
with open(os.path.join(sys.path[0],'nre.conf'), 'rb') as f:
        d = eval(f.read())
token = d['token']
origin = d['origin']
destination = d['destination']
rws = d['rows']		#Max 4 to fit 128x32 screen, 8 for 128x64
arrivals = d['arrivals']

try:
	False
	darwin_ses = DarwinLdbSession(wsdl=wsdlu, api_key=token)
	board = darwin_ses.get_station_board(origin, rows=rws, destination_crs=destination, include_arrivals=arrivals, include_departures=True)
	dict={}
	for x,service in enumerate(board.train_services):
		dict[x]=[service.std, service.destination_text, service.etd]
	with open(os.path.join(sys.path[0], '_nre.dat'), 'w') as h:
		json.dump(dict,h)
except:
	print "%s - Error fetching data from National Rail" % time.strftime("%Y-%m-%d %H:%I:%S")
