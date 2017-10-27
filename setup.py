from setuptools import setup

setup(name="looker_api",
    version=1.0,
    description="Python wrapper for the Looker API",
    url="https://github.com/nickymikail/looker-api",
    author="Nicholas Hassell",
    author_email="hasselln@gmail.com",
    license="MIT",
    install_requires=[
        'requests'
    ],
    packages=['looker_api'],
    keywords = ['business intelligence', 'bi', 'looker'])