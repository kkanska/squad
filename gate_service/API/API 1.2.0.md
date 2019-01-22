```graphql
# User profile description
type UserProfile {
  avatarURL: String
  description: String
}

# User output format
type User {
  userID: Int
  login: String
  email: String
  profile: UserProfile
  avgRating: Float
  ratingsNo: Int
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

enum DisciplineName {
  FOOTBALL
  VOLLEYBALL
}

# Type of match
type Category {
  name: DisciplineName
  imageURL: String
}

# Type of match input format
input CategoryRef {
  name: DisciplineName
}

# User settings output format
type UserSettings {
  defaultDiscipline: Category
  notificationIntervals: [Float]
  sendNotifications: Boolean
  defaultLocation: Location
  defaultRange: Float
}

# User settings input format
input UserSettingsRef {
  defaultDiscipline: CategoryRef
  notificationIntervals: [Float]
  sendNotifications: Boolean
  defaultLocation: LocationRef
  defaultRange: Float
}

# Date output format
type Date {
  timestamp: String
}

# Date input format
input DateRef {
  timestamp: String
}

# Match details
type Match {
  matchID: Int
  title: String
  date: Date
  location: Location
  author: User
  administrator: User
  category: Category
  maxPlayers: Int
  minPlayers: Int
  players: [User]
  invited: [User]
  timeToCompleteSquad: Date
  votingThreshold: Int
}

# Match data input format
input MatchPreferences {
  title: String
  date: DateRef
  location: LocationRef
  author: UserRef
  administrator: UserRef
  category: CategoryRef
  maxPlayers: Int
  minPlayers: Int
  players: [UserRef]
  invited: [UserRef]
  timeToCompleteSquad: DateRef
  votingThreshold: Int
}

# Query matches data
type MatchesQuery {
  getActiveMatches(user: UserRef): [Match]  # ITERATION1
  searchMatches(author: UserRef, date: DateRef, location: LocationRef, range: Float): [Match]  # ITERATION1, DateRef indicates one day
  getCommonMatches(user: UserRef, coplayer: UserRef): [Match]
}

# User invitation type
type Invite {
  matchID: Int
  from: User
  inviteID: Int
}

# Result of the server action
type ActionResult {
  message: String
  isOK: Boolean
}

# Match/users actions
type ActionsMutation {
  registerUser(email: String, login: String, hash: String): User  # ITERATION1
  createNewMatch(user: UserRef, matchPreferences: MatchPreferences): Int  # ITERATION1
  inviteUser(user: UserRef, toInvite: UserRef, matchID: Int): ActionResult  # ITERATION2
  joinMatch(user: UserRef, matchID: Int): ActionResult  # ITERATION1
  leaveMatch(user: UserRef, matchID: Int): ActionResult  # ITERATION2
  changeAdministrator(user: UserRef, newAdmin: UserRef, matchID: Int): ActionResult  # ITERATION2
  changeLocation(user: UserRef, newLocation: LocationRef, matchID: Int): ActionResult  # ITERATION2
  changeDate(user: UserRef, newDate: DateRef, matchID: Int): ActionResult  # ITERATION2
  changePlayerLimits(user: UserRef, newMinPlayers: Int, newMaxPlayers: Int, matchID: Int): ActionResult  # ITERATION2
  changeVotingThreshold(user: UserRef, newVotingThreshold: Int, matchID: Int): ActionResult
  changeTimeToCompleteSquad(user: UserRef, newTime: DateRef, matchID: Int): ActionResult  # ITERATION2
  blockUser(user: UserRef, toBeBlocked: UserRef, matchID: Int): ActionResult
  kickUser(user: UserRef, kickedUser: UserRef, matchID: Int): ActionResult
}

# Query user settings
type SettingsQuery {
  getSettings(user: UserRef): UserSettings  # ITERATION1
}

# Change user settings
type SettingsMutation {
  changeSettings(user: UserRef, newSettings: UserSettingsRef): ActionResult  # ITERATION2
}

# Query user data
type UsersQuery {
  findUsers(login: String, email: String, id: Int, limit: Int): [User]  # ITERATION2
  getCommonPlayers(user: UserRef, coplayer: UserRef): [User]
  getCoplayers(user: UserRef): [User]
}

# Invite users
type InvitesQuery {
  getInvites(user: UserRef): [Invite]  # ITERATION2
}

# Invite users actions
type InvitesMutation {
  respondToInvite(user: UserRef, inviteID: Int, response: Boolean): ActionResult  # ITERATION2
}

# Main query type
type Query {
  authorizeUser(email: String, hash: String): User  # ITERATION1
  matches: MatchesQuery
  settings: SettingsQuery
  users: UsersQuery
  invites: InvitesQuery
}

# Main mutation type
type Mutation {
  actions: ActionsMutation
  settings: SettingsMutation
  invites: InvitesMutation
  dropTables(authKey: String) : ActionResult
}

```