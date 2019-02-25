#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name="backent",
    version="1.0.0",
    author="Victor Perron",
    author_email="victor@iso3103.net",
    description="A backend for events",
    license="CC-BY-SA",
    keywords="",
    url="",
    packages=find_packages(exclude=['tests*']),
    python_requires='>=3.4.2',
    include_package_data=True,
    install_requires=[
        'dj-database-url>=0.4.1',
        'Django>=2',
        'psycopg2>=2.6.2',
        'whitenoise>=3.3.0',
        'djangorestframework',
        'django-countries',
        'pillow',
        'dateparser',
        'fuzzywuzzy',
        'requests',
        'django-widget-tweaks',
        'django-cors-headers',
        'django-map-widgets',
        'python-google-places',
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Natural Language :: French",
        "Programming Language :: Python :: 3.5",
    ],
)
