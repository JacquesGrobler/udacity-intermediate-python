"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.
"""
import csv
import json

from helpers import cd_to_datetime, datetime_to_str


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output
    row corresponds to the information in a single close approach from the
    `results` stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data
    should be saved.
    """
    fieldnames = ('datetime_utc', 'distance_au', 'velocity_km_s',
                  'designation', 'name', 'diameter_km',
                  'potentially_hazardous')

    with open(filename, 'w') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            final_output = {'datetime_utc': row.time,
                            'distance_au': row.distance,
                            'velocity_km_s': row.velocity,
                            'designation': row.neo.designation,
                            'name': row.neo.name,
                            'diameter_km': row.neo.diameter,
                            'potentially_hazardous': row.neo.hazardous}
            if final_output['name'] is None:
                final_output['name'] = ''
            else:
                final_output['name'] = final_output['name']
            if final_output['diameter_km'] is None:
                final_output['diameter_km'] = 'nan'
            else:
                final_output['diameter_km'] = final_output['diameter_km']
            if final_output['potentially_hazardous'] == 'Y':
                final_output['potentially_hazardous'] = 'True'
            else:
                final_output['potentially_hazardous'] = 'False'
            writer.writerow(final_output)


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly,
    the output is a list containing dictionaries, each mapping
    `CloseApproach` attributes to their values and the 'neo' key
    mapping to a dictionary of the associated NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data
    should be saved.
    """
    final = [{'datetime_utc': datetime_to_str(row.time),
              'distance_au': float(row.distance),
              'velocity_km_s': float(row.velocity),
              'neo': {
                'designation': row.neo.designation,
                'name': row.neo.name if row.neo.name else '',
                'diameter_km': row.neo.diameter if row.neo.diameter else 'nan',
                'potentially_hazardous': row.neo.hazardous}}
             for row in results]

    with open(filename, 'w') as outfile:
        json.dump(final, outfile, indent=2)
