import time
from math import sin, cos, sqrt, atan2, radians


LOCATIONS = {'Centrum Sportu i Rekreacji UW': {'lng': 52.2075519, 'lat': 20.9737179},
             'Hala Sportowa Szkoła': {'lng': 52.2075665, 'lat': 20.9637277},
             'Międzyszkolny Ośrodek Sportowy nr 7': {'lng': 52.2079872, 'lat': 20.971195},
             'MIM UW': {'lng': 52.2118767, 'lat': 20.9799491}}


def milli_time(hours_delta=0):
    return str(int(round((time.time() + hours_delta) * 1000)))


def dist(coords1, coords2):
    # https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
    # approximate radius of earth in m
    R = 6373000.0

    lat1 = radians(coords1['lat'])
    lon1 = radians(coords1['lng'])
    lat2 = radians(coords2['lat'])
    lon2 = radians(coords2['lng'])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


users = {
    1: {'login': 'piotrek',
         'email': 'piotrek@gmail.com',
         'profile': {'avatar_url': 'data:image/png;base64,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',
                     'description': 'Jestem sobie Piotrek.'},
         'settings': {'default_range': 1500.,
                      'default_discipline': {'name': 'Piłka nożna'},
                      'default_location': LOCATIONS['MIM UW']},
         'hash': 'psswrd'},
    2: {'login': 'kasia',
         'email': 'kasia@gmail.com',
         'profile': {'avatar_url': 'data:image/png;base64,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',
                     'description': 'Jestem sobie Kasia.'},
         'settings': {'default_range': 1400.,
                      'default_discipline': {'name': 'Piłka nożna'},
                      'default_location': LOCATIONS['MIM UW']},
         'hash': 'psswrd'},
    3: {'login': 'stasiek',
         'email': 'stasiek@gmail.com',
         'profile': {'avatar_url': 'data:image/png;base64,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',
                     'description': 'Jestem sobie Stasiek.'},
         'settings': {'default_range': 1600.,
                      'default_discipline': {'name': 'Piłka nożna'},
                      'default_location': LOCATIONS['MIM UW']},
         'hash': 'psswrd'},
    4: {'login': 'alex',
         'email': 'alex@gmail.com',
         'profile': {'avatar_url': 'data:image/png;base64,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',
                     'description': 'Jestem sobie Alex.'},
         'settings': {'default_range': 1200.,
                      'default_discipline': {'name': 'Piłka nożna'},
                      'default_location': LOCATIONS['MIM UW']},
         'hash': 'psswrd'},
}


USERS_COUNT = 4


def find_hash_and_id(email):
    for key, value in users.items():
        if value['email'] == email:
            return value['hash'], key

    return None, None


matches = {
    1: {
        'title': 'Międzyszkolny Ośrodek Sportowy nr 7',
        'min_players': 10,
        'max_players': 20,
        'voting_threshold': 5,
        'date': {'timestamp': milli_time(5)},
        'location': LOCATIONS['Międzyszkolny Ośrodek Sportowy nr 7'],
        'author': 1,
        'administrator': 1,
        'category': {'name': 'Piłka nożna'},
        'players': [1, 2, 3],
        'invited': [4],
        'time_to_complete_squad': {'timestamp': milli_time(4)}
    },
    2: {
        'title': 'Centrum Sportu i Rekreacji UW',
        'min_players': 10,
        'max_players': 20,
        'voting_threshold': 5,
        'date': {'timestamp': milli_time(8)},
        'location': LOCATIONS['Centrum Sportu i Rekreacji UW'],
        'author': 1,
        'administrator': 1,
        'category': {'name': 'Piłka nożna'},
        'players': [1, 2],
        'invited': [3, 4],
        'time_to_complete_squad': {'timestamp': milli_time(7)}
    },
    3: {
        'title': 'Hala Sportowa Szkoła',
        'min_players': 10,
        'max_players': 20,
        'voting_threshold': 5,
        'date': {'timestamp': milli_time(15)},
        'location': LOCATIONS['Hala Sportowa Szkoła'],
        'author': 1,
        'administrator': 1,
        'category': {'name': 'Piłka nożna'},
        'players': [1, 2, 3],
        'invited': [4],
        'time_to_complete_squad': {'timestamp': milli_time(14)}
    },
    4: {
        'title': 'Hala Sportowa Szkoła',
        'min_players': 10,
        'max_players': 20,
        'voting_threshold': 5,
        'date': {'timestamp': milli_time(12)},
        'location': LOCATIONS['Hala Sportowa Szkoła'],
        'author': 1,
        'administrator': 1,
        'category': {'name': 'Piłka nożna'},
        'players': [1, 2, 3],
        'invited': [4],
        'time_to_complete_squad': {'timestamp': milli_time(11)}
    },
    5: {
        'title': 'Międzyszkolny Ośrodek Sportowy nr 7',
        'min_players': 10,
        'max_players': 20,
        'voting_threshold': 5,
        'date': {'timestamp': milli_time(25)},
        'location': LOCATIONS['Międzyszkolny Ośrodek Sportowy nr 7'],
        'author': 2,
        'administrator': 2,
        'category': {'name': 'Piłka nożna'},
        'players': [2],
        'invited': [1],
        'time_to_complete_squad': {'timestamp': milli_time(24)}
    },
    6: {
        'title': 'Centrum Sportu i Rekreacji UW',
        'min_players': 10,
        'max_players': 20,
        'voting_threshold': 5,
        'date': {'timestamp': milli_time(8)},
        'location': LOCATIONS['Centrum Sportu i Rekreacji UW'],
        'author': 3,
        'administrator': 3,
        'category': {'name': 'Piłka nożna'},
        'players': [3, 4],
        'invited': [1, 2],
        'time_to_complete_squad': {'timestamp': milli_time(7)}
    },
    7: {
        'title': 'Hala Sportowa Szkoła',
        'min_players': 10,
        'max_players': 20,
        'voting_threshold': 5,
        'date': {'timestamp': milli_time(34)},
        'location': LOCATIONS['Hala Sportowa Szkoła'],
        'author': 1,
        'administrator': 1,
        'category': {'name': 'Piłka nożna'},
        'players': [1, 2, 3],
        'invited': [4],
        'time_to_complete_squad': {'timestamp': milli_time(33)}
    },
    8: {
        'title': 'Hala Sportowa Szkoła',
        'min_players': 10,
        'max_players': 20,
        'voting_threshold': 5,
        'date': {'timestamp': milli_time(22)},
        'location': LOCATIONS['Hala Sportowa Szkoła'],
        'author': 1,
        'administrator': 1,
        'category': {'name': 'Piłka nożna'},
        'players': [1, 2, 3],
        'invited': [4],
        'time_to_complete_squad': {'timestamp': milli_time(21)}
    },
}
