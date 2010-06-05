#!/usr/bin/env python
# coding=utf-8
import sys
import gtk
import gtk.gdk
import pygtk
import gnomeapplet
import traffic_applet

pygtk.require('2.0')
gtk.gdk.threads_init()

def applet_factory(applet, iid):
    traffic_applet.TrafficApplet(applet, iid)
    return True
 
if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == '--run-in-window':
            window = gtk.Window(gtk.WINDOW_TOPLEVEL)
            window.set_title('Traffic Monitor')
            window.connect('destroy', gtk.main_quit)
            applet = gnomeapplet.Applet()
            applet_factory(applet, None)
            applet.reparent(window)
            window.show_all()
            gtk.main()
            sys.exit()
        elif sys.argv[1] == '--help':
            print '''
            --run-in-window - run the applet in a window
            --help - show this message'''
    else:
        gnomeapplet.bonobo_factory('OAFIID:GNOME_TrafficApplet_Factory',
                                   traffic_applet.TrafficApplet.__gtype__,
                                   'Traffic Applet',
                                   '0.9',
                                   applet_factory)
