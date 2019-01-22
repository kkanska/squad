from graphene.test import Client
from graphene import Schema
import unittest
import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))
from schema import Query, Mutation

def getSchema():
  return Schema(query=Query, mutation=Mutation)
  
def getClient():
  return Client(getSchema())
  
def graphQLExecute(query, variables, client=None):
  if not client:
    client = getClient()
  executed = client.execute(query, variable_values=variables)
  return executed
  
def assertEquality(x, y):
  if x != y:
    print('Expected:')
    print(x)
    print('Got:')
    print(y)
    assert False