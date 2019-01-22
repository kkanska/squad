from helper import *

class TestRegister(unittest.TestCase):

    #
    # Try to register new user
    #
    def test_register(self):
      assertEquality(graphQLExecute(
        '''
          mutation Mutation($userEmail: String, $userLogin: String, $userHash: String) {
            actions {
              registerUser(email: $userEmail, login: $userLogin, hash: $userHash) {
                email
              }
            }
          }
        ''',
        {
          'userLogin': 'none',
          'userHash': 'e73249888w90dhsuh3iuh2h2s23434',
          'userEmail': 'none@nope.com'
        }
      ), {
        'data': {
          'actions': {
            'registerUser': {
              'email': 'none@nope.com'
            }
          }
        }
      })