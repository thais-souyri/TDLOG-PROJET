from typing import Dict
Day = str
DayPeriod = str
PostType = str





PLANNING_EXAMPLE: Dict[Day, Dict[DayPeriod, Dict[PostType, int]]] = {'lundi': {
    'matin': {'pickeur rack': 6, 'pickeur etagere': 2, 'operateur skypod': 3, 'agent logistique ventilation': 5,
              'agent logistique conduceteur de ligne emballage': 3, 'agent logistique palettisation': 2},
    'après-midi': {'pickeur rack': 6, 'pickeur etagere': 7, 'operateur skypod': 7,
                   'agent logistique ventilation': 1, 'agent logistique conduceteur de ligne emballage': 5,
                   'agent logistique palettisation': 0}}, 'mardi': {
    'matin': {'pickeur rack': 0, 'pickeur etagere': 4, 'operateur skypod': 3, 'agent logistique ventilation': 2,
              'agent logistique conduceteur de ligne emballage': 0, 'agent logistique palettisation': 6},
    'après-midi': {'pickeur rack': 5, 'pickeur etagere': 5, 'operateur skypod': 3,
                   'agent logistique ventilation': 6, 'agent logistique conduceteur de ligne emballage': 2,
                   'agent logistique palettisation': 7}}, 'mercredi': {
    'matin': {'pickeur rack': 1, 'pickeur etagere': 3, 'operateur skypod': 5, 'agent logistique ventilation': 7,
              'agent logistique conduceteur de ligne emballage': 5, 'agent logistique palettisation': 7},
    'après-midi': {'pickeur rack': 0, 'pickeur etagere': 4, 'operateur skypod': 7,
                   'agent logistique ventilation': 2, 'agent logistique conduceteur de ligne emballage': 5,
                   'agent logistique palettisation': 0},
    'nuit': {'pickeur rack': 6, 'pickeur etagere': 3, 'operateur skypod': 4, 'agent logistique ventilation': 1,
             'agent logistique conduceteur de ligne emballage': 2, 'agent logistique palettisation': 5}}, 'jeudi': {
    'matin': {'pickeur rack': 5, 'pickeur etagere': 3, 'operateur skypod': 5, 'agent logistique ventilation': 5,
              'agent logistique conduceteur de ligne emballage': 2, 'agent logistique palettisation': 4},
    'après-midi': {'pickeur rack': 5, 'pickeur etagere': 3, 'operateur skypod': 3,
                   'agent logistique ventilation': 0, 'agent logistique conduceteur de ligne emballage': 5,
                   'agent logistique palettisation': 5}}, 'vendredi': {
    'matin': {'pickeur rack': 5, 'pickeur etagere': 4, 'operateur skypod': 4, 'agent logistique ventilation': 4,
              'agent logistique conduceteur de ligne emballage': 2, 'agent logistique palettisation': 5},
    'après-midi': {'pickeur rack': 7, 'pickeur etagere': 5, 'operateur skypod': 5,
                   'agent logistique ventilation': 2, 'agent logistique conduceteur de ligne emballage': 6,
                   'agent logistique palettisation': 7}}, 'samedi': {
    'matin': {'pickeur rack': 5, 'pickeur etagere': 5, 'operateur skypod': 6, 'agent logistique ventilation': 6,
              'agent logistique conduceteur de ligne emballage': 2, 'agent logistique palettisation': 3},
    'après-midi': {'pickeur rack': 3, 'pickeur etagere': 7, 'operateur skypod': 4,
                   'agent logistique ventilation': 1, 'agent logistique conduceteur de ligne emballage': 4,
                   'agent logistique palettisation': 4},
    'nuit': {'pickeur rack': 4, 'pickeur etagere': 6, 'operateur skypod': 4, 'agent logistique ventilation': 2,
             'agent logistique conduceteur de ligne emballage': 6, 'agent logistique palettisation': 7}},
    'dimanche': {
        'matin': {'pickeur rack': 6, 'pickeur etagere': 1, 'operateur skypod': 5, 'agent logistique ventilation': 1,
                  'agent logistique conduceteur de ligne emballage': 4, 'agent logistique palettisation': 0},
        'après-midi': {'pickeur rack': 5, 'pickeur etagere': 5, 'operateur skypod': 6,
                       'agent logistique ventilation': 1, 'agent logistique conduceteur de ligne emballage': 4,
                       'agent logistique palettisation': 5},
        'nuit': {'pickeur rack': 1, 'pickeur etagere': 5, 'operateur skypod': 7, 'agent logistique ventilation': 0,
                 'agent logistique conduceteur de ligne emballage': 1, 'agent logistique palettisation': 3}}}

PLANNING_EXAMPLE2={'lundi': {
    'matin': {'Picking': 6,'Packaging': 3, 'Palletization': 2},
    'après-midi': {'Picking': 6,'Packaging': 5,
                   'Palletization': 0}}, 'mardi': {
    'matin': {'Picking': 0,
              'Packaging': 0, 'Palletization': 6},
    'après-midi': {'Picking': 5, 'Packaging': 2,
                   'Palletization': 7}}, 'mercredi': {
    'matin': {'Picking': 1,
              'Packaging': 5, 'Palletization': 7},
    'après-midi': {'Picking': 0, 'Packaging': 5,
                   'Palletization': 0},
    'nuit': {'Picking': 6,
             'Packaging': 2, 'Palletization': 5}}, 'jeudi': {
    'matin': {'Picking': 5,
              'Packaging': 2, 'Palletization': 4},
    'après-midi': {'Picking': 5, 'Packaging': 5,
                   'Palletization': 5}}, 'vendredi': {
    'matin': {'Picking': 5,
              'Packaging': 2, 'Palletization': 5},
    'après-midi': {'Picking': 7, 'Packaging': 6,
                   'Palletization': 7}}, 'samedi': {
    'matin': {'Picking': 5,
              'Packaging': 2, 'Palletization': 3},
    'après-midi': {'Picking': 3, 'Packaging': 4,
                   'Palletization': 4},
    'nuit': {'Picking': 4,
             'Packaging': 6, 'Palletization': 7}},
    'dimanche': {
        'matin': {'Picking': 6,
                  'Packaging': 4, 'Palletization': 0},
        'après-midi': {'pickeur rack': 5,  'Packaging': 4,
                       'Palletization': 5},
        'nuit': {'Picking': 1,
                 'Packaging': 1, 'Palletization': 3}}}
RETURN_EXAMPLE=(PLANNING_EXAMPLE2,25,147)
DAYS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"]
POSTS = ["pickeur rack", "pickeur etagere", "operateur skypod", "agent logistique ventilation",
         "agent logistique conduceteur de ligne emballage", "agent logistique palettisation"]

POSTS2=["Picking", "Packaging", "Palletization"]
MONTHS = ["Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre",
          "Novembre", "Décembre"]
