from distutils.core import setup

setup(name='Traffic Applet',
      version='0.9',
      description='Gnome Panel applet for monitoring your traffic.',
      author='MyFreeWeb',
      url='http://github.com/myfreeweb/gnome-traffic-applet/',
      data_files=[
                  ('/usr/bin', ['traffic_factory.py']),
                  ('/usr/lib/bonobo/servers', ['GNOME_TrafficApplet.server']),
                 ],
     )
