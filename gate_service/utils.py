import time
import requests
import json
import config
from models import *


def str_timestamp():
    return str(time.time())


def str_to_dict(s):
    return json.loads(s.replace('\'', '\"'))


def get_usr_from_data(json_data):
    profile_kwargs = default_profile()

    return User(user_id=json_data['id'], login=json_data['login'], email=json_data['email'],
                profile=UserProfile(**profile_kwargs))


def get_usr_data_by_id(usr_id):
    r = requests.get(config.USER_ADDR + '/api/users/{}'.format(usr_id))
    if r.status_code != 200:
        return None

    return r.json()


def get_usr_by_id(usr_id):
    usr = get_usr_data_by_id(usr_id)
    if not usr:
        return None

    return get_usr_from_data(usr)


def get_usr_sett_by_id(usr_id):
    usr = get_usr_data_by_id(usr_id)
    if not usr:
        return None

    location = Location(lat=usr.get('sett_default_lat', 20.9799491),
                        lng=usr.get('sett_default_lng', 52.2118767))

    category_name = CategoryName.get(usr.get('sett_category_name', 0))
    discipline = Category(name=category_name,
                          icon_name=usr.get('sett_category_icon', None))

    return UserSettings(default_range=usr.get('sett_default_range', 1500.),
                        default_location=location,
                        default_discipline=discipline,
                        timestamp=usr.get('sett_timestamp', None))


def get_match_from_data(match_data):
    players = []
    for player_id in match_data['players']:
        player = get_usr_by_id(player_id)
        if player:
            players.append(player)

    invited = []
    for player_id in match_data['invited']:
        player = get_usr_by_id(player_id)
        if player:
            invited.append(player)

    return Match(match_id=match_data['id'], date=Date(timestamp=match_data['date']),
                 location=Location(lat=match_data['location_lat'], lng=match_data['location_lng']),
                 author=get_usr_by_id(match_data['author_id']),
                 administrator=get_usr_by_id(match_data['author_id']),
                 category=Category(name=CategoryName(match_data['category'])),
                 players=players, invited=invited)


def default_profile():
    return {'avatar_url': config.DEFAULT_AVATAR,
            'avg_ratings': 0.5,
            'ratings_no': 10,
            }


def default_settings():
    return {'default_range': config.DEFAULT_RANGE,
            'default_discipline': config.DEFAULT_DISCIPLINE,
            'default_location': config.DEFAULT_LOCATION}


def coord_to_postgis(lng, lat):
    return "SRID=4326;POINT ({} {})".format(lat, lng)


def request_service(service, url, method, data):
    # default service is MATCHES
    req = {'put': lambda kwargs: requests.put(**kwargs),
           'post': lambda kwargs: requests.post(**kwargs),
           'patch': lambda kwargs: requests.patch(**kwargs),
           'get': lambda kwargs: requests.get(**kwargs),
           }

    kwargs = {'data': json.dumps(data),
              'headers': {'content-type': 'application/json'},
              }

    if service == "AUTH":
        kwargs['url'] = '{}/{}'.format(config.AUTH_ADDR, url)
    elif service == "USER":
        kwargs['url'] = '{}/{}'.format(config.USER_ADDR, url)
    else:
        kwargs['url'] = '{}/{}'.format(config.MATCHES_ADDR, url)
    print('Sending request to {}'.format(kwargs['url']))

    return req[method](kwargs)
