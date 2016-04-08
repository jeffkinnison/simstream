"""
    Setup for simstream module.

    Author: Jeff Kinnison (jkinniso@nd.edu)
"""

from disutils.core import setup

setup(
    name="simstream",
    version="0.1dev",
    author="Jeff Kinnison",
    author_email="jkinniso@nd.edu",
    packages=["simstream"],
    description=""
    install_requires=[
        "tornado >= 4.3"
    ],
)
