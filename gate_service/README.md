# Gate Microservice

```graphql

#
# GATE API
#

# User profile description
type UserProfile {
  # Should be valid url or event data-type url (e.g. base64 encoded image)
  avatarURL: String
  
  # Must be 0 <= avgRating <= 1
  avgRating: Float
  ratingsNo: Int
  
  # UNUSED
  description: String
}

# User output format
type User {
  userID: Int!
  login: String!
  email: String!
  profile: UserProfile
}

# User input format
input UserRef {
  userID: Int
  login: String
}

# Location output format
type Location {
  lat: Float
  lng: Float
}

# Location input format
input LocationRef {
  lat: Float
  lng: Float
}

# Disciplines types
enum DisciplineName {
  FOOTBALL
  VOLLEYBALL
}

# Type of match
type Category {
  name: DisciplineName!
  
  # Note that it's not the icon url or data-type url (e.g. base64) encoding
  # The icon name should be valid Ionicons name
  # For full list of icon icons see:
  #  
  #     https://ionicframework.com/docs/ionicons/ 
  #
  iconName: String
}

# Type of match input format
input CategoryRef {
  name: DisciplineName
}

# User settings output format
type UserSettings {
  defaultDiscipline: Category
  defaultLocation: Location
  defaultRange: Float
  timestamp: String
  
  # UNUSED
  notificationIntervals: [Float]
  
  # UNUSED
  sendNotifications: Boolean
}

# User settings input format
input UserSettingsRef {
  defaultDiscipline: CategoryRef
  defaultLocation: LocationRef
  defaultRange: Float
  
  # UNUSED
  notificationIntervals: [Float]
  
  # UNUSED
  sendNotifications: Boolean
}

# Date output format
type Date {
  timestamp: String!
}

# Date input format
input DateRef {
  timestamp: String!
}

# Match details
type Match {
  matchID: Int!
  title: String
  date: Date
  location: Location
  author: User
  administrator: User
  category: Category
  players: [User]!
  invited: [User]!
  
  # UNUSED
  timeToCompleteSquad: Date
  
  # UNUSED
  votingThreshold: Int
  
  # UNUSED
  maxPlayers: Int
  
  # UNUSED
  minPlayers: Int
}

# Match data input format
input MatchPreferences {
  title: String
  date: DateRef
  location: LocationRef
  author: UserRef
  administrator: UserRef
  category: CategoryRef
  players: [UserRef]
  invited: [UserRef]
  
  # UNUSED
  maxPlayers: Int
  
  # UNUSED
  minPlayers: Int
  
  # UNUSED
  timeToCompleteSquad: DateRef
  
  # UNUSED
  votingThreshold: Int
}

# Optional suggestions sent by server to increase
# number of search results
type MatchFilterSuggestion {
  # If range is not-nulled then the user will see visual components that after some kind of interaction
  # will resend the query to the server with that range specified.
  # For example server may return range for which numer of matches is > 3 for the specified location
  # then it will help user to search for more matches with single interaction (e.g. click etc.)
  range: Float
}

# Search results with optional suggestions
type MatchSearchResult {
  # Found matches
  matches: [Match]!
  
  # Optional suggestions for better searching
  # If this object is non-nulled
  # then it will be used for presenting visual feedback for user to increase quality of the search
  # For more details see MatchFilterSuggestion type
  suggestions: [MatchFilterSuggestion]
}

# Query matches data
type MatchesQuery {
  # Currently active matches of the <user>
  getActiveMatches(user: UserRef): [Match]!  # ITERATION1
  
  # Search matches
  # <date> is single-day date
  # Note that all paramteres are optional and can be nulled
  searchMatches(author: UserRef, date: DateRef, location: LocationRef, range: Float): MatchSearchResult!  # ITERATION1, DateRef indicates one day
  
  # UNUSED
  getCommonMatches(user: UserRef, coplayer: UserRef): [Match]!
}

# User invitation type
type Invite {
  match: Match
  from: User
  inviteID: Int!
}

# Type with information that can identify the user
input IDSpecs {
  # Timestamp of data generation
  timestamp:  String!
  
  # Hash for device identification (should be const per device)
  deviceHash: String!
  
  # Device ID loaded from software
  deviceID:   String!
  
  # Human readable device name
  deviceName: String!
  
  # Session ID that identifies apilication instance
  # This don't have to be unique across multiple devices
  sessionID:  String!
}

# Result of the server action
type ActionResult {
  # Optional human readable server response
  message: String
  
  # Server status (True = 0K, False = Troubles)
  isOK: Boolean!
}

# Match/users actions
type ActionsMutation {

  # New user signs up with the given email, login and password hash
  registerUser(email: String, login: String, hash: String): User  # ITERATION1
  
  # <user> creates new match
  createNewMatch(user: UserRef, matchPreferences: MatchPreferences): Int  # ITERATION1
  
  # <user> invites new user <toInvite> to the match
  inviteUser(user: UserRef, toInvite: UserRef, matchID: Int): ActionResult!  # ITERATION2
  
  # New <user> joins match
  joinMatch(user: UserRef, matchID: Int): ActionResult!  # ITERATION1
  
  # <user> leaves the match
  leaveMatch(user: UserRef, matchID: Int): ActionResult!  # ITERATION2
  
  # Modify match administrator
  changeAdministrator(user: UserRef, newAdmin: UserRef, matchID: Int): ActionResult!  # ITERATION2
  
  # Modify location of match
  changeLocation(user: UserRef, newLocation: LocationRef, matchID: Int): ActionResult!  # ITERATION2
  
  # Modify match date
  changeDate(user: UserRef, newDate: DateRef, matchID: Int): ActionResult!  # ITERATION2
  
  # UNUSED
  changePlayerLimits(user: UserRef, newMinPlayers: Int, newMaxPlayers: Int, matchID: Int): ActionResult!
  
  # UNUSED
  changeVotingThreshold(user: UserRef, newVotingThreshold: Int, matchID: Int): ActionResult!
  
  # UNUSED
  changeTimeToCompleteSquad(user: UserRef, newTime: DateRef, matchID: Int): ActionResult!
  
  # UNUSED
  blockUser(user: UserRef, toBeBlocked: UserRef, matchID: Int): ActionResult!
  
  # UNUSED
  kickUser(user: UserRef, kickedUser: UserRef, matchID: Int): ActionResult!
  
  # <user> ranks user <rankedUser> in context of match <matchID>
  # rating must be valid [0, 1] rank value
  rankUser(user: UserRef, rankedUser: UserRef, matchID: Int, rating: Float): ActionResult! # ITERATION 2
}

# Query user settings
type SettingsQuery {
  # Obtain <user>'s settings
  getSettings(user: UserRef): UserSettings  # ITERATION1
}

# Change user settings
type SettingsMutation {
  # Partial or full scope modification of <user>'s settings
  changeSettings(user: UserRef, newSettings: UserSettingsRef): ActionResult!  # ITERATION2
}

# Query user data
type UsersQuery {
  # Get the mark of user <rankedUser> that was reported by <user> for match <matchID>
  # Valid values are in range [0, 1]
  # All others will be assumed to signal that user was not ranked
  getYourRankOfUser(user: UserRef, rankedUser: UserRef, matchID: Int): Float # ITERATION 2
  
  # Fuzzy search of users using input <text>
  findUsers(text: String, limit: Int): [User]!  # ITERATION2
  
  # UNUSED
  getCommonPlayers(user: UserRef, coplayer: UserRef): [User]!
  
  # UNUSED
  getCoplayers(user: UserRef): [User]!
}

# Invite users
type InvitesQuery {
  # Obtain all invites received by <user>
  getInvites(user: UserRef): [Invite]!  # ITERATION2
}

# Invite users actions
type InvitesMutation {
  # <user> reponds to invite
  # reponse = True means accept invitation
  # reponse = False means deny invitation
  respondToInvite(user: UserRef, inviteID: Int, response: Boolean): ActionResult!  # ITERATION2
}

# Main query type
type Query {
  # Login user using his <email> and password <hash>
  # idspecs is identification specification object used to identify
  # the exact session/device of user (see input type IDSpecs for more details)
  authorizeUser(email: String, hash: String, idspecs: IDSpecs): User  # ITERATION1
  
  matches: MatchesQuery!
  settings: SettingsQuery!
  users: UsersQuery!
  invites: InvitesQuery!
}

# Main mutation type
type Mutation {
  actions: ActionsMutation!
  settings: SettingsMutation!
  invites: InvitesMutation!
  
  # UNUSED
  dropTables(authKey: String): ActionResult!
}


```
