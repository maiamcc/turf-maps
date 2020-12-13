#! /usr/bin/env python

import csv
from typing import Dict, List

import simplekml

TRANSPARENT_PIN = 'https://www.gstatic.com/mapspro/images/stock/503-wht-blank_maps.png'
COLORS = [
    simplekml.constants.Color.aqua,
    simplekml.constants.Color.crimson,
    simplekml.constants.Color.darkgreen,
    simplekml.constants.Color.darkgoldenrod,
    simplekml.constants.Color.darkorchid,
    simplekml.constants.Color.coral,
]
COLOR_LIT_HUB = simplekml.constants.Color.black
COLOR_UNAVAILABLE = simplekml.constants.Color.lightgray

KEY_NAME = "Name"
KEY_REGION = "Region"
KEY_LON = "Lon"
KEY_LAT = "Lat"
KEY_AVAILABLE = "Available"

VAL_LIT_HUB = "Lit Hub"


def new_point_with_color(kml_doc: simplekml.Kml, name: str, lon: int, lat: int, color: simplekml.constants.Color):
    pnt = kml_doc.newpoint(name=name, coords=[(lon, lat)])
    pnt.style.iconstyle.icon.href = TRANSPARENT_PIN  # rm stupid default pin icon
    pnt.style.iconstyle.color = color


def map_regions_to_colors(data: List[Dict]):
    regions = set(row[KEY_REGION] for row in data if row[KEY_REGION] != VAL_LIT_HUB)
    if len(regions) > len(COLORS):
        raise Exception('Whoops designate some more colors')

    color_map = {VAL_LIT_HUB: COLOR_LIT_HUB}
    for i, r in enumerate(regions):
        color_map[r] = COLORS[i]

    return color_map


data = []
with open('sample_turf.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data.append(row)

colors_for_region = map_regions_to_colors(data)

doc = simplekml.Kml()
for row in data:
    color = colors_for_region[row[KEY_REGION]]
    if row[KEY_AVAILABLE] != 'y':
        color = COLOR_UNAVAILABLE
    new_point_with_color(doc, row[KEY_NAME], row[KEY_LON], row[KEY_LAT], color)

doc.save('sample_turf.kml')