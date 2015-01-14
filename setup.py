#!/usr/bin/env python3

import os
from setuptools import setup

from rc import __client__, __version__

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = __client__,
    version = __version__,
    author = "Brent Strysko",
    author_email = "bstrysko@andrew.cmu.edu",
    description = ("CMU Robotics Club API"),
    license = "MIT",
    keywords = "roboclub robotics club api cmu",
    packages=['rc/',],
    scripts = ["bin/rc-api"],
    long_description=read('README.md'),
    install_dependencies = ['requests', 'python-dateutil']
)