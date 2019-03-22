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
    Shop.objects.all().delete()
    FrenchDepartment.objects.all().delete()
    ShopRegion.objects.all().delete()
    ShopNetwork.objects.all().delete()

    for dct in read_csv_data(args.region_filename):
        ShopRegion.objects.create(
            pk=int(dct['reg_id']),
            name=clean(dct['reg_nom']),
            legacy_google=int(dct['reg_google']),
            description=clean(dct['reg_desc']),
            coords=Point(float(dct['reg_long']), float(dct['reg_lat'])),
        )

    for dct in read_csv_data(args.departments_filename):
        try:
            name = clean(dct['dpt_name'])
            region = int(dct['region'])
            FrenchDepartment.objects.create(
                pk=int(dct['dpt_id']),
                name=name,
                region=ShopRegion.objects.get(pk=region),
            )
        except (ValueError, ShopRegion.DoesNotExist):
            print(">>>>>>> error: department=%s region=%s does not exist" % (name, region))
            continue

    for dct in read_csv_data(args.network_filename):
        ShopNetwork.objects.create(
            pk=int(dct['r_id']),
            name=clean(dct['r_nom']),
            description=clean(dct['r_desc']),
            webpage=dct['r_url']
        )

    for dct in read_csv_data(args.shops_filename):
        try:
            network = ShopNetwork.objects.get(pk=int(dct['m_reseau']))
        except (ValueError, ShopNetwork.DoesNotExist):
            network = None

        region_id  = dct['m_region']
        try:
            region = ShopRegion.objects.get(pk=int(region_id))
        except (ValueError, ShopRegion.DoesNotExist):
            print(">>>>>>> error: shop=%s region=%s does not exist" % (dct['m_nom'], region_id))
            continue

        dpt = clean(dct['m_dpt'])
        if dpt not in ALL_DEPARTMENTS:
            print(">>>>>>> error: shop=%s department=%s does not exist" % (dct['m_nom'], dpt))
            continue
        phone = clean(dct['m_tel'])
        if phone == '-':
            phone = None
        else:
            phone = '+33' + phone.replace(' ', '')

        shop = Shop.objects.create(
            pk=int(dct['m_id']),
            network=network,
            name=clean(dct['m_nom']),
            description=clean(dct['m_intro']),
            highlights=clean(dct['m_special']),
            address=clean(dct['m_addr1']),
            zipcode=clean(dct['m_cp']),
            city=clean(dct['m_ville']),
            state=clean(dct['m_dpt']),
            region=ShopRegion.objects.get(pk=int(dct['m_region'])),
            coords=Point(float(dct['m_longitude']), float(dct['m_latitude'])),
            webpage=dct['m_web'],
            email=clean(dct['m_mail_mag']),
            phone=phone,
            organic_level=clean(dct['m_bio']),
        )
        img_name = 'shop_%s.png' % int(dct['m_id'])
        with open('scripts/shop-images/%s' % img_name, 'rb') as f:
            shop.picture.save("%s.png" % dct['m_id'], File(f))

    for dct in read_csv_data(args.users_filename):
        # "u_id","u_mail","u_mail_valid","u_pwd","u_valid","u_type","u_magid","u_tmp_magid","u_annee","u_sexe","u_pseudo","u_cp","u_visites","u_last_visit","u_creation","u_key","u_prod_fiche","u_tel"
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
