from flask import Flask, jsonify, abort, request
import redis
import json

app = Flask(__name__)

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    '''Getting user by id'''
    user=r.hgetall('users:{}'.format(user_id))
    if user == {}:
        return abort(404)
    user['id'] = user_id

    return jsonify(user), 200

@app.route('/api/users/', methods=['POST'])
def create_user():
    '''Creating new user and returning id'''
    new_id=r.incr('id:users')

    user_data=request.json
    print(user_data)
    r.hmset('users:{}'.format(new_id), user_data)

    user_data['id']=new_id

    return jsonify(user_data), 201

@app.route('/api/users/<int:user_id>', methods=['PATCH'])
def alter_user(user_id):
    '''Changing some of user data'''


    data_to_change=request.json

    r.hmset('users:{}'.format(user_id), data_to_change)
    user_data=r.hgetall('users:{}'.format(user_id))

    user_data['id']=user_id
    return jsonify(user_data), 202

@app.route('/api/rank/<int:user_id>', methods=['PATCH'])
def rank_user(user_id):

    data = request.json
    rating = data['rating']
    match_id = data['match_id']

    # TODO Rank user in database, save amount of reviewers



if __name__ == '__main__':
    r=redis.Redis(host='storage', port=6379, db=0, decode_responses=True)
    app.run(debug=True,host='0.0.0.0', port=5000)
