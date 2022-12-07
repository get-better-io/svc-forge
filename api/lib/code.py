"""
Contains the Models for {{ service }}
"""

import time
import relations

class Base(relations.Model):
    """
    Base class for "{{ service }}" models
    """

    SOURCE = "{{ service }}"

def now():
    """
    Time function so we can freeze
    """
    return time.time()

class Item(Base):
    """
    Item Model
    """

    id = int
    name = str
    labels = set
    tags = dict
    meta = dict
