"""
Extract data on near-Earth objects and close approaches.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided
at the command line, and uses the resulting collections
to build an `NEODatabase`.
"""

import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data
    about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    neos = []
    with open(neo_csv_path, 'r') as infile:
        reader = csv.reader(infile)
        next(reader)
        for row in reader:
            neo = {}
            neo['designation'] = row[3]
            neo['name'] = row[4] if row[4] != '' else None
            neo['diameter'] = float(row[15]) if row[15] != '' else float('NaN')
            neo['hazardous'] = row[7]
            neos.append(NearEarthObject(**neo))
    return neos


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data
    about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    cads = []
    with open(cad_json_path, 'r') as file:
        data = json.load(file)['data']
        for row in data:
            cad = {}
            cad['designation'] = row[0]
            cad['time'] = row[3]
            cad['distance'] = float(row[4]) if row[4] != '' else float('NaN')
            cad['velocity'] = float(row[7]) if row[7] != '' else float('NaN')
            cads.append(CloseApproach(**cad))
    return cads
