"""
File:               persistor_type.py
Description:        Enumeration of persistors used by the Knowledge Factory, and beyond.
Created on:         04-june-2022 11:25:00
Author:             SEMBU Team - NTTData Barcelona
"""
from enum import IntEnum


class PersistorType (IntEnum):
    """
    Defines the persistor types
    """
    NONE = 0
    FILE = 1
    VIRTUOSO = 2
    GRAPHDB = 3
    STARDOG = 4
    ELASTIC = 5
    MONGODB = 6
    RSQL = 7
