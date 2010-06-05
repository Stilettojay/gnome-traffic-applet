#!/usr/bin/env python
# coding=utf-8
import sys
import gtk
import pygtk
import gnomeapplet
 
pygtk.require('2.0')

class TrafficApplet(gnomeapplet.Applet):
    def __init__(self, applet, iid): 
        self.kb = lambda a: int(a)/1024
        self.applet = applet
        self.applet.set_name('Traffic Applet')
        hbox = gtk.HBox()
        eventbox = gtk.EventBox()
        self.label = gtk.Label()
        self.applet.add(hbox)
        hbox.add(eventbox)
        eventbox.add(self.label)
        self.applet.connect('destroy', self.callback_destroy)
        self.applet.show_all()
        self.label.set_text(self.get_traffic('bnep0')) # TODO: settings
 
    def get_traffic(self, interface):
        try:
            STAT_PATH = '/sys/class/net/' + interface + '/statistics/'
            rxfile = open(STAT_PATH + 'rx_bytes', 'r')
            rx_kb = self.kb(rxfile.read())
            rxfile.close()
            txfile = open(STAT_PATH + 'tx_bytes', 'r')
            tx_kb = self.kb(txfile.read())
            txfile.close()
            return '%s kb / %s kb' % (rx_kb, tx_kb)
        except IOError:
            return 'Offline'

    def callback_destroy(self, applet):
        del self.applet

def applet_factory(applet, iid):
    TrafficApplet(applet, iid)
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
                                   TrafficApplet.__gtype__,
                                   'Traffic Applet',
                                   '0.9',
                                   applet_factory)
