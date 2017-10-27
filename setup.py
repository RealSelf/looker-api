from setuptools import setup

setup(name="looker-api",
    version=1.0,
    description="SDK for the Realself Looker API",
    url="https://looker.com",
    author="Nicholas Hassell",
    author_email="nick.hassell@realself.com",
    license="MIT",
    install_requires=[
        'requests'
    ],
    packages=['looker_api'],
    zip_safe=False)