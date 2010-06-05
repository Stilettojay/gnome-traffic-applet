#!/usr/bin/env python
# coding=utf-8
import time
import threading
import gtk
import gtk.gdk
import pygtk
import gnomeapplet

pygtk.require('2.0')

try:
    import gconf
except ImportError:
    gconf = None

global GCONF_DIR
GCONF_DIR = '/apps/gnome-traffic-applet'

def gconf_client():
    client = gconf.client_get_default()
    client.add_dir(GCONF_DIR, gconf.CLIENT_PRELOAD_NONE)
    return client

class TrafficSettings():
    def __init__(self):
        self.dialog = gtk.Dialog()
        self.dialog.set_title('Traffic Applet Settings')
        try:
            ca = self.dialog.get_content_area()
        except:
            ca = self.dialog.vbox
        
        if gconf:
            global GCONF_DIR
            self.gc_string = GCONF_DIR + '/interface'
            iface_hbox = gtk.HBox()
            iface_label = gtk.Label('Network interface:')
            self.iface_input = gtk.Entry()
            self.iface_input.set_text(gconf_client().get_string(self.gc_string))
            iface_hbox.pack_start(iface_label, False)
            iface_hbox.pack_end(self.iface_input)
            ca.pack_start(iface_hbox, False)
        else:
            ca.add(gtk.Label('Please install python-gconf with your package manager.'))

        self.dialog.connect('response', self.callback_close_dialog)
        self.dialog.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
        self.dialog.show_all()

    def callback_close_dialog(self, *args):
        if gconf:
            client = gconf_client()
            client.set_string(self.gc_string, self.iface_input.get_text())
        self.dialog.destroy()

class TrafficApplet(gnomeapplet.Applet):
    def __init__(self, applet, iid): 
        self.kb = lambda a: int(a)/1024
        self.applet = applet
        self.applet.set_name('Traffic Applet')
        self.applet.setup_menu('''<popup name="button3">
<menuitem name="ItemPreferences"
          verb="Preferences"
          label="_Preferences"
          pixtype="stock"
          pixname="gtk-preferences" />
</popup>''', [('Preferences', self.show_preferences)], None)
        hbox = gtk.HBox()
        eventbox = gtk.EventBox()
        self.label = gtk.Label()
        self.applet.add(hbox)
        hbox.add(eventbox)
        eventbox.add(self.label)
        self.applet.connect('destroy', self.callback_destroy)
        self.applet.show_all()
        self.monitoring_active = True
        self.start_monitoring_thread()

    def start_monitoring_thread(self):
        threading.Thread(target=self.monitoring_loop).start()

    def monitoring_loop(self):
        if gconf:
            global GCONF_DIR
            client = gconf_client()
            client.notify_add(GCONF_DIR + '/interface', self.callback_change_iface)
            self.callback_change_iface(client)
            
        while self.monitoring_active:
            traffic = self.get_traffic(self.network_iface or None)
            if traffic:
                total = traffic[0] + traffic[1]
                self.label.set_text('%s kb' % total)
                self.applet.set_tooltip_text('%s kb down, %s kb up' % traffic)
            else:
                self.label.set_text('Offline')
            time.sleep(1)
            
    def get_traffic(self, interface):
        try:
            if not interface:
                interface = 'eth0' # fallback.
                # if you don't have python-gconf, you can change it here.

            STAT_PATH = '/sys/class/net/' + interface + '/statistics/'
            rxfile = open(STAT_PATH + 'rx_bytes', 'r')
            rx_kb = self.kb(rxfile.read())
            rxfile.close()
            txfile = open(STAT_PATH + 'tx_bytes', 'r')
            tx_kb = self.kb(txfile.read())
            txfile.close()
            return (rx_kb, tx_kb)
        except IOError:
            return False

    def show_preferences(obj, label, *data):
        TrafficSettings()

    def callback_change_iface(self, client, *args):
        global GCONF_DIR
        self.network_iface = client.get_string(GCONF_DIR + '/interface')

    def callback_destroy(self, applet):
        self.monitoring_active = False
        del self.applet
