from utils import *
from requests import ConnectionError
import graphene
from models import *
from config import *


class InviteUser(graphene.Mutation):
    class Arguments:
        inviter_id = UserRef(required=True)
        matchID = graphene.Int(required=True)
        invited = UserRef(required=True)

    message = graphene.String()
    status = graphene.Boolean()

    def mutate(self, info, user, invited, matchID):

        data = {'match': matchID,
                'inviter': user.user_id,
                'invitee': invited.user_id,
                }
        r = request_service('MATCHES', url='invites/', method='put', data=data)
        if r.status_code != 202:
            return InviteUser(message="Failed to invite user {}".format(invited), status=False)

        else:
            return InviteUser(message="User {} successfully invited to match".format(invited), status=True)


class ChangeAdministrator(graphene.Mutation):
    class Arguments:
        user = UserRef(required=True)
        new_admin = UserRef(required=True)
        match_id = graphene.Int(required=True)

    status = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, user, new_admin, match_id):

        data = {'match_id': match_id,
                'user': user,
                'new_admin': new_admin,
                }

        r = request_service('MATCHES', url='matches/admin/', method='put', data=data)
        if r.status_code != 202:
            return ChangeAdministrator(message="Failed to change admin to user {}"
                                       .format(new_admin),
                                       status=False)

        else:
            return ChangeAdministrator(message="User {} successfully granted admin rights"
                                       .format(new_admin),
                                       status=True)


class RespondToInvite(graphene.Mutation):
    class Arguments:
        user = UserRef(required=True)
        invite_id = graphene.Int(required=True)
        response = graphene.Boolean()

    status = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, user, invite_id, response):

        data = {'user': user,
                'invite_id': invite_id,
                'respone': response,
                }

        r = request_service('MATCHES', url='invites/respond/', method='put', data=data)
        if r.status_code != 202:
            return RespondToInvite(message="Failed to change respond to invite", status=False)

        else:
            return RespondToInvite(message="Successfully responded to invite", status=True)


class RegisterUser(graphene.Mutation):
    class Arguments:
        email = graphene.String()
        login = graphene.String()
        hash = graphene.String()

    userID = graphene.Int()
    login = graphene.String()
    status = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, email, login, hash):
        # send request to AUTH to register user and get his id
        # get user data via USERS
        usr_data = {
                'login': login,
                'email': email,
                'password': hash,
                }

        r = request_service('AUTH', url='auth/register', method='post', data=usr_data)
        if r.status_code != 202:
            return RegisterUser(status=False)

        else:
            id = r.json()['id']
            r = request_service('USER', url='api/users/{}'.format(id),
                                method='get', data=usr_data)

            if r.status_code != 200:
                return RegisterUser(status=False)

            else:
                return RegisterUser(login=login, userID=id, status=True)


class JoinMatch(graphene.Mutation):
    class Arguments:
        user = UserRef(required=True)
        matchID = graphene.Int(required=True)

    message = graphene.String()
    isOK = graphene.Boolean()

    def mutate(self, info, user, matchID):
        try:
            data = {'id': matchID,
                    'new_player': user.user_id}
            r = request_service('MATCHES', url='matches/', method='patch', data=data)
            if r.status_code != 202:
                return ActionResult(message='Matches service fail', isOK=False)

            return ActionResult(message='Player successfully updated', isOK=True)

        except ConnectionError:
            return ActionResult(message='Connection error', isOK=False)


class LeaveMatch(graphene.Mutation):
    class Arguments:
        user = UserRef(required=True)
        matchID = graphene.Int(required=True)

    message = graphene.String()
    isOK = graphene.Boolean()

    def mutate(self, info, user, matchID):
        try:
            data = {'id': matchID,
                    'remove_player': user.user_id}
            r = request_service('MATCHES', url='matches/', method='patch', data=data)
            if r.status_code != 202:
                return ActionResult(message='Matches service fail', isOK=False)

            return ActionResult(message='Player successfully updated', isOK=True)

        except ConnectionError:
            return ActionResult(message='Connection error', isOK=False)


class ChangeLocation(graphene.Mutation):
    class Arguments:
        user = UserRef(required=True)
        newLocation = LocationRef(required=True)
        matchID = graphene.Int(required=True)

    message = graphene.String()
    isOK = graphene.Boolean()

    def mutate(self, info, user, newLocation, matchID):
        if not newLocation.lat or not newLocation.lng:
            return ActionResult(message='Location incomplete', isOK=False)

        location_str = coord_to_postgis(lat=newLocation.lat, lng=newLocation.lng)

        try:
            data = {'id': matchID,
                    'location': location_str}
            r = request_service('MATCHES', url='matches/', method='patch', data=data)
            if r.status_code != 202:
                return ActionResult(message='Matches service fail', isOK=False)

            return ActionResult(message='Location successfully updated', isOK=True)

        except ConnectionError:
            return ActionResult(message='Connection error', isOK=False)


class ChangeDate(graphene.Mutation):
    class Arguments:
        user = UserRef(required=True)
        newDate = DateRef(required=True)
        matchID = graphene.Int()

    message = graphene.String()
    isOK = graphene.Boolean()

    def mutate(self, info, user, newDate, matchID):
        if not newDate.timestamp:
            return ActionResult(message='Date incomplete', isOK=False)

        try:
            data = {'id': matchID,
                    'date': newDate.timestamp}
            r = request_service('MATCHES', url='matches/', method='patch', data=data)
            if r.status_code != 202:
                return ActionResult(message='Matches service fail', isOK=False)

            return ActionResult(message='Date successfully updated', isOK=True)

        except ConnectionError:
            return ActionResult(message='Connection error', isOK=False)


class CreateNewMatch(graphene.Mutation):
    class Arguments:
        user = UserRef(required=True)
        matchPreferences = MatchPreferences(required=True)

    matchID = graphene.Int()

    def mutate(self, info, user, matchPreferences):
        data = dict()

        if matchPreferences.location.lat or matchPreferences.location.lng:
            data['location'] = coord_to_postgis(lat=matchPreferences.location.lat,
                                                lng=matchPreferences.location.lng)

        data['author_id'] = user.user_id

        if matchPreferences.date:
            data['date'] = matchPreferences.date.timestamp

        if matchPreferences.category:
            data['discipline'] = matchPreferences.category.name

        new_match_data = {k: v for k, v in data.items() if v is not None}

        if new_match_data:
            try:
                r = request_service('MATCHES', url='matches/', method='post',
                                    data=new_match_data)
                if r.status_code != 201:
                    return CreateNewMatch()

                return CreateNewMatch(matchID=r.json()['id'])

            except ConnectionError:
                return CreateNewMatch()

        return CreateNewMatch()


class ActionsMutation(graphene.Mutation):
    register_user = RegisterUser.Field()
    create_new_match = CreateNewMatch.Field()
    join_match = JoinMatch.Field()
    leave_match = LeaveMatch.Field()
    change_location = ChangeLocation.Field()
    change_date = ChangeDate.Field()

    def mutate(self, info):
        return ActionsMutation()


class RankUser(graphene.Mutation):
    class Arguments:
        user = UserRef(required=True)
        rankedUser = UserRef(required=True)
        match_id = graphene.Int()
        rating = graphene.Float()

    message = graphene.String()
    status = graphene.Boolean()

    def mutate(self, info, user, rankedUser, match_id, rating):
        data = {
                'rating': rating,
                'mathch_id': match_id,
                }
        r = request_service('USER', url='api/rank/{}'.format(rankedUser.user_id),
                            method='patch', data=data)
        if r.status_code != 202:
            return RankUser(status=False, message='Failed to rank user')

        else:
            return RankUser(status=True, message='Successully ranked user')


class ChangeSettings(graphene.Mutation):
    class Arguments:
        user = UserRef()
        newSettings = UserSettingsRef()

    message = graphene.String()
    isOK = graphene.Boolean()

    def mutate(self, info, user, newSettings):
        data = dict()
        data['sett_default_range'] = newSettings.default_range

        if newSettings.default_location:
            data['sett_default_lat'] = newSettings.default_location.lat
            data['sett_default_lng'] = newSettings.default_location.lng

        if newSettings.default_discipline:
            data['sett_category_name'] = newSettings.default_discipline.name
            data['sett_category_icon'] = newSettings.default_discipline.icon_name

        new_usr_data = {k: v for k, v in data.items() if v is not None}

        if new_usr_data:
            new_usr_data['sett_timestamp'] = str_timestamp()

            try:
                r = request_service('USER', url='api/users/{}'.format(user.user_id),
                                    method='patch', data=new_usr_data)
                if r.status_code != 202:
                    return ActionResult(message='Users service fail', isOK=False)

                return ActionResult(message='Settings successfully updated', isOK=True)

            except ConnectionError:
                return ActionResult(message='Connection error', isOK=False)

        return ActionResult(message='Nothing to update', isOK=False)


class SettingsMutation(graphene.Mutation):
    change_settings = ChangeSettings.Field()

    def mutate(self, info):
        return SettingsMutation()
