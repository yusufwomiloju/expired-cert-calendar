from setuptools import setup

setup(
   name='expired-cert-calendar',
   version='1.1',
   description='Tool to create a calendar of expired certificates in ISAM v9.x',
   license="MIT",
   author='Yusuf Womiloju',
   author_email='yusuf.womiloju@ibm.com',
   url='https://github.com/yusufwomiloju/expired-cert-calendar',
   packages=['expired-cert-calendar'],  
   install_requires=['requests', 'ics', 'ibmsecurity']
)