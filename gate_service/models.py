import graphene


class UserProfile(graphene.ObjectType):
    avatar_url = graphene.String(name='avatarURL')
    avg_ratings = graphene.Float()
    ratings_no = graphene.Int()


class UserFields(object):
    user_id = graphene.Int(name='userID')
    login = graphene.String()


class User(graphene.ObjectType, UserFields):
    email = graphene.String()
    profile = graphene.Field(UserProfile)


class UserRef(graphene.InputObjectType, UserFields):
    pass


class LocationFields(object):
    lat = graphene.Float()
    lng = graphene.Float()


class Location(graphene.ObjectType, LocationFields):
    pass


class LocationRef(graphene.InputObjectType, LocationFields):
    pass


class CategoryName(graphene.Enum):
    FOOTBALL = 0
    VOLLEYBALL = 1


class CategoryFields(object):
    name = graphene.Field(CategoryName)


class Category(graphene.ObjectType, CategoryFields):
    icon_name = graphene.String()


class CategoryRef(graphene.InputObjectType, CategoryFields):
    pass


class UserSettingsFields(object):
    default_range = graphene.Float()
    timestamp = graphene.String()


class UserSettings(graphene.ObjectType, UserSettingsFields):
    default_discipline = graphene.Field(Category)
    default_location = graphene.Field(Location)


class UserSettingsRef(graphene.InputObjectType, UserSettingsFields):
    default_discipline = graphene.Field(CategoryRef)
    default_location = graphene.Field(LocationRef)


class DateFields(object):
    timestamp = graphene.String()


class Date(graphene.ObjectType, DateFields):
    pass


class DateRef(graphene.InputObjectType, DateFields):
    pass


class MatchFields(object):
    title = graphene.String()


class Match(graphene.ObjectType, MatchFields):
    match_id = graphene.Int(name='matchID')
    date = graphene.Field(Date)
    location = graphene.Field(Location)
    author = graphene.Field(User)
    administrator = graphene.Field(User)
    category = graphene.Field(Category)
    players = graphene.List(User)
    invited = graphene.List(User)


class MatchPreferences(graphene.InputObjectType, MatchFields):
    date = graphene.Field(DateRef)
    location = graphene.Field(LocationRef)
    author = graphene.Field(UserRef)
    administrator = graphene.Field(UserRef)
    category = graphene.Field(CategoryRef)
    players = graphene.List(UserRef)
    invited = graphene.List(UserRef)


class MatchFilterSuggestion(graphene.ObjectType):
    range = graphene.Float()


class MatchSearchResult(graphene.ObjectType):
    matches = graphene.List(Match)
    suggestions = graphene.List(MatchFilterSuggestion)


class Invite(graphene.ObjectType):
    match = graphene.Field(Match)
    user = graphene.Field(User)
    invite_id = graphene.Int(name="inviteID")


class IDSpecs(graphene.InputObjectType):
    timestamp = graphene.String()
    device_hash = graphene.String()
    device_id = graphene.String(name="deviceID")
    device_name = graphene.String()
    session_id = graphene.String(name="sessionID")


class ActionResult(graphene.ObjectType):
    message = graphene.String()
    isOK = graphene.Boolean()
