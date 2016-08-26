# -*- coding: utf-8 -*-
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject, GLib
GObject.threads_init()
import time
import threading

# debug
debug=1

Udata={}
Ulbs={}

class readlassdata(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
	global Udata
        Udata['pm'] = '10'
        Udata['temp'] = '10'
        Udata['humi'] = '10'
        Udata['light'] = '10'


#class UpdateData(threading.Thread):
class UpdateData():
    def __init__(self, lbs):
	self.lbs = Ulbs
	self.run()

    def run(self):
	if self.access_moodle() == True:
	    self.update_labels()

    def update_labels(self):
	self.lbs['time'].set_text(Udata['time'])
	self.lbs['temp'].set_text("%s °C" % Udata['temp'])
	self.lbs['pm'].set_text("%s μg/m3" % Udata['pm'])
	self.lbs['light'].set_text(Udata['light'])
	self.lbs['humi'].set_text("%s %%" % Udata['humi'])

    def access_moodle(self):

	global Udata
        ctime = time.strftime("%Y/%m/%d\n%H:%M:%S")
	Udata['time'] = ctime
	return True

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
window.connect("delete-event", Gtk.main_quit)
GObject.timeout_add_seconds(1, UpdateData, lbs)
window.show_all()

thrReader = readlassdata()
thrReader.daemon = True
thrReader.start()

Gtk.main()
