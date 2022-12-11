"""
Contains the Models for {{ service }}
"""

import relations

class Base(relations.Model):
    """
    Base class for {{ service }} models
    """

    SOURCE = "{{ service }}"

class Person(Base):
    """
    Person model
    """

    CHUNK = 2

    id = int
    name = str
    status = ["active", "inactive"]


class Stuff(Base):
    """
    Stuff model
    """

    ID = None
    person_id = int
    name = str
    items = list

relations.OneToMany(Person, Stuff)


class Thing(Base):
    """
    Thing model
    """

    id = int
    person_id = int
    name = str
    items = dict

relations.OneToMany(Person, Thing)


class Meta(Base):
    """
    Meta model
    """

    id = int
    name = str
    flag = bool
    spend = float
    people = set
    stuff = list
    things = dict
