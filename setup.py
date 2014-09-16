#!/usr/bin/env python3

import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pyroboclub",
    version = "0.1",
    author = "Brent Strysko",
    author_email = "bstrysko@andrew.cmu.edu",
    description = ("CMU Robotics Club API"),
    license = "MIT",
    keywords = "roboclub robotics club api cmu",
    packages=['rc/', 'tests'],
    scripts = ["bin/rc-api"],
    long_description=read('README.md'),
    install_dependencies = ['requests', ]
)