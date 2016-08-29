# -*- coding: utf-8 -*-
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject, GLib
GObject.threads_init()
import time
import sqlite3

# debug
debug=1

Udata={}
Ulbs={}
db_file="/root/monitor.db"
conn=0
cur=0


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

    def access_moodle(self):

	global Udata
        global db_file

        conn = sqlite3.connect(db_file) 
        cur = conn.cursor() 

        ctime = time.strftime("%Y/%m/%d\n%H:%M:%S")
	Udata['time'] = ctime

        data = cur.execute('SELECT sensor_value FROM monitor WHERE sensor=\'pm2.5\' ORDER BY date DESC limit 1')
        Udata['pm'] = "%2.2f" % float(data.fetchone()[0])
        
        data = cur.execute("SELECT sensor_value FROM monitor WHERE sensor='temp' ORDER BY date DESC limit 1")
        Udata['temp'] = "%2.2f" % float(data.fetchone()[0])

        data = cur.execute("SELECT sensor_value FROM monitor WHERE sensor='humi' ORDER BY date DESC limit 1")
        Udata['humi'] = "%2.2f" % float(data.fetchone()[0])
        Udata['light'] = u''
	#print Udata
    	conn.close()

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
Ulbs=lbs
window.connect("delete-event", close_win)
GObject.timeout_add_seconds(3, UpdateData, lbs)
window.show_all()

Gtk.main()
