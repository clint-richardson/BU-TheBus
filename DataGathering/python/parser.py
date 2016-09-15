
import urllib2
import json
from datetime import datetime

def queryTimes():
    #test = urllib2.urlopen("http://www.bu.edu/bumobile/rpc/bus/stops.json.php?service_id=fall&callback=?").read()
    dict = urllib2.urlopen("http://www.bu.edu/bumobile/rpc/bus/livebus.json.php?callback=?").read()

    test = json.loads(dict)

    stops = []
    buses = []
    nstops=[]
    for key in test:
        if key =='ResultSet':
            results = test[key]
            result = results['Result']
            for k in result:
                for j in k:
                    if j=='arrival_estimates':
                        stops.append(k[j])                   
                        nstops.append(len(k[j]))
                    if j=='call_name' and ('arrival_estimates' in k):
                        buses.append(k[j])
                         

    times=[]
    stopIDs = []
    routes =[]

    for stop in stops:
        for i in stop:
            for key in i:
                if key =='arrival_at':
                    times.append(i[key])
                elif key == 'stop_id':
                    stopIDs.append(i[key])
                elif key == 'route_id':
                    routes.append(i[key])

    entries = []
    it=0
    count=0
    for i in range(0,len(nstops)):
        bus = buses[i]
        for j in range( count, count+nstops[i]):
            time = times[j]
            time=time.replace('-04:00','')
            time=time.replace('T',' ')
            now = datetime.now()
            entry = bus+','+str(now)+','+time+','+stopIDs[it]+','+routes[it]
            entries.append(entry)
            it+=1
        count+=nstops[i]

    fout = open('times.csv','a')
    for entry in entries:
        fout.write(entry+'\n')

    fout.close()

import time

while True:
    print 'Querying BU bus data at %s' % str(datetime.now())
    queryTimes()
    time.sleep(30)
