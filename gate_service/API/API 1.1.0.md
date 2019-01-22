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

# Type of match
type Category {
  name: String
}

# Type of match input format
input CategoryRef {
  name: String
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
  getActiveMatches(user: UserRef): [Match]
  searchMatches(author: UserRef, date: DateRef, location: LocationRef, range: Float): [Match]
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
  registerUser(email: String, login: String, hash: String): User
  createNewMatch(user: UserRef, matchPreferences: MatchPreferences): Int
  inviteUser(user: UserRef, toInvite: UserRef, matchID: Int): ActionResult
  joinMatch(user: UserRef, matchID: Int): ActionResult
  leaveMatch(user: UserRef, matchID: Int): ActionResult
  changeAdministrator(user: UserRef, newAdmin: UserRef, matchID: Int): ActionResult
  changeLocation(user: UserRef, newLocation: LocationRef, matchID: Int): ActionResult
  changeDate(user: UserRef, newDate: DateRef, matchID: Int): ActionResult
  changePlayerLimits(user: UserRef, newMinPlayers: Int, newMaxPlayers: Int, matchID: Int): ActionResult
  changeVotingThreshold(user: UserRef, newVotingThreshold: Int, matchID: Int): ActionResult
  changeTimeToCompleteSquad(user: UserRef, newTime: DateRef, matchID: Int): ActionResult
  blockUser(user: UserRef, toBeBlocked: UserRef, matchID: Int): ActionResult
  kickUser(user: UserRef, kickedUser: UserRef, matchID: Int): ActionResult
}

# Query user settings
type SettingsQuery {
  getSettings(user: UserRef): UserSettings
}

# Change user settings
type SettingsMutation {
  changeSettings(user: UserRef, newSettings: UserSettingsRef): ActionResult
}

# Query user data
type UsersQuery {
  findUsers(login: String, email: String, id: Int, limit: Int): [User]
  getCommonPlayers(user: UserRef, coplayer: UserRef): [User]
  getCoplayers(user: UserRef): [User]
}

# Invite users
type InvitesQuery {
  getInvites(user: UserRef): [Invite]
}

# Invite users actions
type InvitesMutation {
  respondToInvite(user: UserRef, inviteID: Int, response: Boolean): ActionResult
}

# Main query type
type Query {
  authorizeUser(email: String, hash: String): User
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
}

```