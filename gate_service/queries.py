from utils import *
import graphene
from types import *
from requests import ConnectionError
from models import *


class MatchesQuery(graphene.ObjectType):
    get_active_matches = graphene.List(Match, user=graphene.Argument(UserRef))
    search_matches = graphene.List(Match, author=graphene.Argument(UserRef), date=graphene.Argument(DateRef),
                                   location=graphene.Argument(LocationRef), range=graphene.Argument(graphene.Float))

    def resolve_get_active_matches(self, info, user=None):
        if user:
            usr_sett = get_usr_sett_by_id(user.user_id)
            r = request_service('MATCHES', url='matches/?radius={}&lat={}&lng={}&date={}'
                                .format(usr_sett.default_range,
                                        usr_sett.default_location.lat,
                                        usr_sett.default_location.lng,
                                        str_timestamp()),
                                method='get', data={})
            if r.status_code != 200:
                return []
            else:
                matches = r.json()
                return [get_match_from_data(match_data) for match_data in matches]
        else:
            return []

    def resolve_search_matches(self, info, author=None, date=None, location=None, range=None):
        r = request_service('MATCHES', url='matches/?radius={}&lat={}&lng={}&date={}'
                            .format(range if range else 5000.,
                                    location.lat if location else '',
                                    location.lng if location else '',
                                    date.timestamp if date else ''),
                            method='get', data={})
        if r.status_code != 200:
            return []

        matches = r.json()
        return [get_match_from_data(match_data) for match_data in matches]


class SettingsQuery(graphene.ObjectType):
    get_settings = graphene.Field(UserSettings, user=graphene.Argument(UserRef, required=True))

    def resolve_get_settings(self, info, user):
        try:
            return get_usr_sett_by_id(user.user_id)

        except ConnectionError:
            return UserSettings()


class UsersQuery(graphene.ObjectType):
    getYourRankOfUser = graphene.Field(graphene.Float, user=graphene.Argument(UserRef),
                                       rankedUser=graphene.Argument(UserRef),
                                       matchID=graphene.Argument(graphene.Int))
    findUsers = graphene.List(User,
                              text=graphene.Argument(graphene.String),
                              limit=graphene.Argument(graphene.Int))
    getCommonPlayers = graphene.List(User,
                                     user=graphene.Argument(User),
                                     coplayer=graphene.Argument(UserRef))
    getCoplayers = graphene.List(User,
                                 user=graphene.Argument(UserRef))


class InvitesQuery(graphene.ObjectType):
    get_invites = graphene.List(Invite, user=graphene.Argument(UserRef))

    def resolve_get_invites(self, info, user):
        r = request_service('MATCHES', url='invites/?invitee={}'.format(user.user_id),
                            method='get', data={})
        if r.status_code != 200:
            return []

        else:
            invites = r.json()
            return [Invite(match=i.match_id, user=i.invitee, invite_id=i.id) for i in invites]
