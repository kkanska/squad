from queries import *
from mutations import *

# TODO: document nicely (see http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)
# TODO: python vs js variable naming (match_id vs matchID)


class Query(graphene.ObjectType):
    authorize_user = graphene.Field(User, email=graphene.Argument(graphene.String, required=True),
                                    hash=graphene.Argument(graphene.String, required=True),
                                    idspecs=graphene.Argument(IDSpecs, required=True))
    matches = graphene.Field(MatchesQuery)
    settings = graphene.Field(SettingsQuery)

    def resolve_authorize_user(self, info, email, hash, idspecs):
        # authorize user using email, hash via AUTH
        # get user from USERS by id
        data = {'email': email,
                'password': hash,
                }

        r = request_service('AUTH', url='auth/login', method='post', data=data)
        if r.status_code != 200:
            return None

        else:
            id = r.json()['id']
            return get_usr_by_id(id)

    def resolve_matches(self, info):
        return MatchesQuery()

    def resolve_settings(self, info):
        return SettingsQuery()


class Mutation(graphene.ObjectType):
    actions = ActionsMutation.Field()
    settings = SettingsMutation.Field()
