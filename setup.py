#!/usr/bin/env python
from distutils.core import setup

setup(name='Traffic Applet',
      version='0.9',
      description='Gnome Panel applet for monitoring your traffic.',
      author='MyFreeWeb',
      url='http://github.com/myfreeweb/gnome-traffic-applet/',
      packages=[
                 'traffic_applet',
               ],
      scripts=[
                'traffic_factory.py',
              ],
      data_files=[
                   ('/usr/lib/bonobo/servers', ['GNOME_TrafficApplet.server']),
                 ],
)
