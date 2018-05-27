__author__ = "Thomas Fischer"

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name="simpletcp",
      author="Thomas Fischer",
      author_email="",
      url="http://github.com/fschr/simpletcp",
      version="1.0.3",
      license="GNU AFFERO GENERAL PUBLIC LICENSE Version 3.0",
      description="Simple non-blocking TCP communcation.",
      keywords="tcp server non-blocking async asynchronous socket",
      packages=["simpletcp",]
      )
