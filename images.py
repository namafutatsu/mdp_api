#!/usr/bin/env python3

import argparse
import csv
import html
import os
from os import path

import django
import django.db.utils
from django.core.files import File
from django.contrib.gis.geos import Point

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mdp_api.settings')
os.environ.setdefault('SECRET_KEY', 'caca')

django.setup()

from mdp_api.api.models import Shop


if __name__ == '__main__':
    for shop in Shop.objects.all():
        print(shop.picture.url)
