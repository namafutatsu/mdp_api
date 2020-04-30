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

from mdp_api.models import User
from mdp_api.api import enums
from mdp_api.api.models import Shop, ShopNetwork, ShopRegion, FrenchDepartment


ALL_DEPARTMENTS = [item[0] for item in enums.FRENCH_DEPARTMENTS]


def read_csv_data(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        return [row for row in reader]


def clean(s):
    return html.unescape(s.strip()).replace('<br>', '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Inject CSV processed complete data into the SQL database.')
    parser.add_argument('region_filename', metavar='REGION_FILE NAME', help='the input regions CSV filename')
    parser.add_argument('network_filename', metavar='NETWORK_FILE NAME', help='the input networks CSV filename')
    parser.add_argument('shops_filename', metavar='SHOPS_FILE NAME', help='the input shops CSV filename')
    parser.add_argument('users_filename', metavar='USERS_FILE NAME', help='the input users CSV filename')
    parser.add_argument('departments_filename', metavar='DEPARTMENTS_FILE NAME', help='the input departments CSV filename')
    args = parser.parse_args()

    User.objects.all().delete()

    for dct in read_csv_data(args.users_filename):
        try:
            email = clean(dct['u_mail'])
            username = clean(dct['u_pseudo'])
            user = User.objects.create(
                pk=int(dct['u_id']),
                email=email,
                username=username,
                has_newsletter=bool(dct['u_mail_valid']),
            )
        except django.db.utils.IntegrityError:
            print(">>>>>>> error: username=%s email=%s already exists" % (username, email))
            continue
        user.set_password(dct['u_pwd'])
        shop_id = int(dct['u_magid']) or int(dct['u_tmp_magid'])
        if shop_id != 0:
            try:
                shop = Shop.objects.get(pk=shop_id)
                user.shop = shop
            except (ValueError, Shop.DoesNotExist):
                print(">>>>>>> error: user=%s shop=%s does not exist" % (user.email, shop_id))
                continue
        user.save()
