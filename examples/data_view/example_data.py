# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Example data generation functions

This module provides some routines for randomly generating data for use
in examples.
"""

from random import choice, randint, uniform

from pyface.color import Color


male_names = [
    'Michael', 'Edward', 'Timothy', 'James', 'George', 'Ralph', 'David',
    'Martin', 'Bryce', 'Richard', 'Eric', 'Travis', 'Robert', 'Bryan',
    'Alan', 'Harold', 'John', 'Stephen', 'Gael', 'Frederic', 'Eli', 'Scott',
    'Samuel', 'Alexander', 'Tobias', 'Sven', 'Peter', 'Albert', 'Thomas',
    'Horatio', 'Julius', 'Henry', 'Walter', 'Woodrow', 'Dylan', 'Elmer',
]

female_names = [
    'Leah', 'Jaya', 'Katrina', 'Vibha', 'Diane', 'Lisa', 'Jean', 'Alice',
    'Rebecca', 'Delia', 'Christine', 'Marie', 'Dorothy', 'Ellen', 'Victoria',
    'Elizabeth', 'Margaret', 'Joyce', 'Sally', 'Ethel', 'Esther', 'Suzanne',
    'Monica', 'Hortense', 'Samantha', 'Tabitha', 'Judith', 'Ariel', 'Helen',
    'Mary', 'Jane', 'Janet', 'Jennifer', 'Rita', 'Rena', 'Rianna',
]

all_names = male_names + female_names

family_names = [
    'Jones', 'Smith', 'Thompson', 'Hayes', 'Thomas', 'Boyle', "O'Reilly",
    'Lebowski', 'Lennon', 'Starr', 'McCartney', 'Harrison', 'Harrelson',
    'Steinbeck', 'Rand', 'Hemingway', 'Zhivago', 'Clemens', 'Heinlien',
    'Farmer', 'Niven', 'Van Vogt', 'Sturbridge', 'Washington', 'Adams',
    'Bush', 'Kennedy', 'Ford', 'Lincoln', 'Jackson', 'Johnson',
    'Eisenhower', 'Truman', 'Roosevelt', 'Wilson', 'Coolidge', 'Mack',
    'Moon', 'Monroe', 'Springsteen', 'Rigby', "O'Neil", 'Philips',
    'Clinton', 'Clapton', 'Santana', 'Midler', 'Flack', 'Conner', 'Bond',
    'Seinfeld', 'Costanza', 'Kramer', 'Falk', 'Moore', 'Cramdon', 'Baird',
    'Baer', 'Spears', 'Simmons', 'Roberts', 'Michaels', 'Stuart',
    'Montague', 'Miller',
]


def any_name():
    return choice(all_names)


def family_name():
    return choice(family_names)


def age():
    return randint(15, 72)


def favorite_color():
    return Color(hsv=(uniform(0.0, 1.0), 1.0, 1.0))


def street():
    number = randint(11, 999)
    text_1 = choice([
        'Spring', 'Summer', 'Moonlight', 'Winding', 'Windy', 'Whispering',
        'Falling', 'Roaring', 'Hummingbird', 'Mockingbird', 'Bluebird',
        'Robin', 'Babbling', 'Cedar', 'Pine', 'Ash', 'Maple', 'Oak', 'Birch',
        'Cherry', 'Blossom', 'Rosewood', 'Apple', 'Peach', 'Blackberry',
        'Strawberry', 'Starlight', 'Wilderness', 'Dappled', 'Beaver', 'Acorn',
        'Pecan', 'Pheasant', 'Owl'
    ])
    text_2 = choice([
        'Way', 'Lane', 'Boulevard', 'Street', 'Drive', 'Circle', 'Avenue',
        'Trail',
    ])
    return '%d %s %s' % (number, text_1, text_2)


def city():
    return choice(['Boston', 'Bristol', 'Cambridge', 'Newcastle', 'York'])


def country():
    return choice(['Canada', 'USA', 'UK'])
