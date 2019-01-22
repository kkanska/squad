from helper import *

class TestAuthorize(unittest.TestCase):

    #
    # Try to authorize user that does not exist
    # This should fail miserably
    #
    def test_invalid_authorization(self):
      assert graphQLExecute(
        '''
          query Query($email: String!, $hash: String!) {
            authorizeUser(email: $email, hash: $hash) {
              userID
            }
          }
        ''',
        {
          'hash': 'e73249888w90dhsuh3iuh2h2s23434',
          'email': 'none@nope.com'
        }
      ) == {
        'data': {
          'authorizeUser': None
        }
      }