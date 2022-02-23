"""
A database encapsulating collections of near-Earth objects and approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.
"""

from models import NearEarthObject, CloseApproach
import functools


class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """

    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        As a precondition, this constructor assumes that the collections
        of NEOs and close approaches haven't yet been linked - that is, the
        `.approaches` attribute of each `NearEarthObject` resolves to an empty
        collection, and the `.neo` attribute of each `CloseApproach` is None.

        However, each `CloseApproach` has an attribute (`._designation`) that
        matches the `.designation` attribute of the corresponding NEO.
        This constructor modifies the supplied NEOs and close approaches
        to link them together - after it's done, the `.approaches` attribute
        of each NEO has a collection of that NEO's close approaches,
        and the `.neo` attribute of each close approach
        references the appropriate NEO.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._neos = neos
        self._approaches = approaches
        self._designation_cache = self.create_designation_chache()
        self._name_cache = self.create_name_chache()
        self._approaches = self.update_approach_neo()

    @functools.lru_cache(maxsize=None)
    def create_designation_chache(self):
        """Create a new dictionary with designation as key.

        The approaches attribute (list) in each neo gets populated
        with associated approaches in the second for loop.

        :return: dicttionary with designation as key and
        neo (in dictionary form) as value.
        """
        _designation_cache = {}
        for neo in self._neos:
            des_key = neo.designation
            if des_key not in _designation_cache:
                _designation_cache[des_key] = neo

        for approach in self._approaches:
            key = approach._designation
            if key in _designation_cache:
                approach.neo = _designation_cache[key]
                if approach not in _designation_cache[key].approaches:
                    _designation_cache[key].approaches.append(approach)
        return _designation_cache

    @functools.lru_cache(maxsize=None)
    def update_approach_neo(self):
        """Update the neo attribute for each approach."""
        updated_approaches = []
        for approach in self._approaches:
            key = approach._designation
            if key in self._designation_cache:
                approach.neo = self._designation_cache[key]
            updated_approaches.append(approach)
        return updated_approaches

    @functools.lru_cache(maxsize=None)
    def create_name_chache(self):
        """Create a new dictionary with name as key.

        :return: dicttionary with name as key and
        neo (in dictionary form) as value.
        """
        _name_cache = {}
        for neo in self._designation_cache.values():
            if neo.name:
                name_key = neo.name
                if name_key not in _name_cache:
                    _name_cache[name_key] = neo
        return _name_cache

    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation,
        or `None`.
        """
        if designation in self._designation_cache:
            return self._designation_cache[designation]
        else:
            return None

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        if name in self._name_cache:
            return self._name_cache[name]
        else:
            return None

    def query(self, filters=()):
        """
        Query close approaches to with the provided filters.

        This generates a stream of `CloseApproach` objects
        that match all of the provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order,
        which isn't guaranteed to be sorted meaninfully,
        although is often sorted by time.

        :param filters: A collection of filters capturing
        user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        for approach in self._approaches:
            criteria_passed = []
            for f in filters:
                criteria_passed.append(f(approach))
            if False not in criteria_passed:
                yield approach
