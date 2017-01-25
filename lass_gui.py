# -*- coding: utf-8 -*-
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject, GLib
GObject.threads_init()
import time
import sqlite3
import urllib2, urllib, json
import os
import re

# debug
debug=1

Udata={}
Ulbs={}
db_file="./monitor.db"


#class UpdateData(threading.Thread):
class UpdateData():
    def __init__(self, lbs):
	self.lbs = Ulbs
	self.run()

    def run(self):
	if self.access_moodle() == True:
	    self.update_labels()
	#self.update_labels()

    def update_labels(self):
        ctime = time.strftime("%Y/%m/%d\n%H:%M:%S")
	Udata['time'] = ctime
	self.lbs['time'].set_text(Udata['time'])
	self.lbs['temp'].set_text(u"%s °C" % Udata['temp'])
	self.lbs['pm'].set_text(u"%s μg/m3" % Udata['pm'])
	self.lbs['light'].set_text(Udata['light'])
	self.lbs['humi'].set_text(u"%s %%" % Udata['humi'])
	x = 1
#	for wx in Udata['forecast']:
	UF=Udata['forecast']
	print UF
	for wxid in range(10):
	    wx = UF[wxid]
	    #print wx
	    datelabel = "ldate%s" % x
	    datestr = wx['date']
	    datestr = datestr.replace("2017", "")
	    self.lbs[datelabel].set_text(datestr)

	    templabel = "ltemp%s" % x
	    tempstr = "%s ~ %s" % (wx['high'], wx['low'])
	    self.lbs[templabel].set_text(tempstr)

	    codelabel = "lcode%s" % x
	    codepath = "./icon/yahoo_weather_icon/%s.gif" % wx['code']
	    print codepath
	    self.lbs[codelabel].set_from_file(codepath)
	    x = x+1

    def access_moodle(self):

	global Udata
        global db_file

        conn = sqlite3.connect(db_file) 
        cur = conn.cursor() 

        ctime = time.strftime("%Y/%m/%d\n%H:%M:%S")
	Udata['time'] = ctime

        data = cur.execute('SELECT sensor_value FROM monitor WHERE sensor=\'pm25\' ORDER BY date DESC limit 1')
        Udata['pm'] = "%2.2f" % float(data.fetchone()[0])
        
        data = cur.execute("SELECT sensor_value FROM monitor WHERE sensor='temp' ORDER BY date DESC limit 1")
        Udata['temp'] = "%2.2f" % float(data.fetchone()[0])

        data = cur.execute("SELECT sensor_value FROM monitor WHERE sensor='humi' ORDER BY date DESC limit 1")
        Udata['humi'] = "%2.2f" % float(data.fetchone()[0])
        Udata['light'] = u''
    	conn.close()

	datafile = 'data.txt'
	Udata['forecast'] = []
	if os.path.isfile(datafile) == False:
	    print "file %s not exist" % datafile

	    baseurl = "https://query.yahooapis.com/v1/public/yql?"
	    yql_query = "select item.condition from weather.forecast where woeid=2306185 and u='c'"
	    yql_query = "select * from weather.forecast where woeid=2306185 and u='c'"
	    yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
	    result = urllib2.urlopen(yql_url).read()
	    with open(datafile, 'w') as outfile:
		json.dump(result, outfile)
	    print "file writed"
	else:
	    print "file %s exist" % datafile
	    with open(datafile, 'r') as json_data:
		sdata = json.load(json_data)
		data = json.loads(sdata)
		forecast = data['query']['results']['channel']['item']['forecast']
		Udata['forecast'] = forecast

        return True

# close win
def close_win():
    Gtk.main_quit

builder = Gtk.Builder()
builder.add_from_file("icon/lass-rpi.glade")

window = builder.get_object("topwin")
ltime = builder.get_object("time")
ltemp = builder.get_object("temp")
lhumi = builder.get_object("humi")
llight = builder.get_object("light")
lpm = builder.get_object("pm")
lbs = {'time':ltime, 'temp':ltemp, 'humi':lhumi, 'light':llight, 'pm':lpm}
for xid in range(10):
    xid = xid+1
    kx = "ldate%s" % xid
    x = builder.get_object("date%s" % xid)
    lbs[kx] = x
    kx = "ltemp%s" % xid
    x = builder.get_object("temp%s" % xid)
    lbs[kx] = x
    kx = "lcode%s" % xid
    x = builder.get_object("code%s" % xid)
    lbs[kx] = x

Ulbs=lbs
window.connect("delete-event", close_win)
GObject.timeout_add_seconds(3, UpdateData, lbs)
window.show_all()

Gtk.main()
