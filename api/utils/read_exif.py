#!/usr/bin/python
# -*- coding:utf-8 -*-
from __future__ import division, unicode_literals

import json
import urllib.request
from decimal import Decimal
from fractions import Fraction

from django.conf import settings
from wand.image import Image

tag = {}


def get_exif_dumps(url):
    """ [{}] list of dict"""
    with Image(file=urllib.request.urlopen(url)) as i:
        for key, value in i.metadata.items():
            if key.startswith('exif:'):
                tag[key] = value
        tags = json.dumps([tag])
    return tags


def get_exif_loads(url):
    """tags[0]['exif:ResolutionUnit']"""
    tags = json.loads(url)
    return tags


def get_exif_path_url(image):
    url = "{0}{1}".format(str(settings.MEDIA_URL), str(image))
    return url


def convert_degress_to_decimal(value):
    data = value.split(",")

    d0 = Fraction(data[0])
    d = float(d0)

    m0 = Fraction(data[1])
    m = float(m0)

    s0 = Fraction(data[2])
    s = float(s0)

    result = d + (m / 60) + (s / 3600)
    data_result = Decimal(result).quantize(Decimal('1.000000'))
    return float(data_result)
