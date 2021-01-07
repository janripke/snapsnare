import logging
from flask import request, current_app
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from snapsnare.system import hasher, tracer, responsify
from snapsnare.repositories.user.user_repository import UserRepository


class Auth(Resource):

    def post(self):
        try:
            payload = request.get_json(silent=True)

            if not payload:
                return responsify(message='Invalid JSON content, or content-type header '
                                          'is not set to application/json'), 400

            username = payload.get('username')
            password = payload.get('password')

            if not username:
                logging.debug('no username given')
                return responsify(message='invalid username or password'), 400

            if not password:
                logging.debug('no password given')
                return responsify(message='invalid username or password'), 400

            connector = current_app.connector
            user_repository = UserRepository(connector)
            user = user_repository.find_by_username(username)

            if not user:
                logging.debug('user not found')
                return responsify(message='invalid username or password'), 400

            # hash the given password, so it can be checked against the hashed password
            # stored in the database
            password = hasher.sha256(password)

            if password != user.get('password'):
                logging.debug('invalid password')
                return responsify(message='invalid username or password'), 401

            access_token = create_access_token(identity=username)

            return responsify(access_token=access_token), 200
        except Exception:
            response = tracer.build()
            logging.exception('authentication failed')
            return response, 500



